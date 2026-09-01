from celery import shared_task
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.db import transaction
from .models import Word, Category
import csv
import io
import os
import logging
import time

logger = logging.getLogger(__name__)

# Custom exceptions for better Flower logging
class ImportError(Exception):
    """Base exception for import errors"""
    pass

class CategoryExistsError(ImportError):
    """Raised when category already exists"""
    pass

class NoWordsCreatedError(ImportError):
    """Raised when no new words were imported"""
    pass

class InvalidFileError(ImportError):
    """Raised when file is invalid or empty"""
    pass


@shared_task(bind=True, max_retries=3)
def import_words_from_csv_task(self, file_path, original_filename, user_id, delimiter=';'):
    """
    Import CSV words with rollback if no new words are created
    """
    # Validate user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        error_msg = f"User {user_id} not found"
        logger.error(error_msg)
        return {
            'status': 'failed',
            'message': error_msg,
            'created': 0,
            'errors': [error_msg],
            'total_lines': 0
        }

    # Validation counters
    stats = {
        'processed': 0,
        'created': 0,
        'skipped_comments': 0,
        'skipped_empty': 0,
        'errors': []
    }

    try:
        with transaction.atomic():
            # 1. Read and validate file
            try:
                content = default_storage.open(file_path, 'r').read()
                if not content:
                    raise InvalidFileError("File is empty")
            except Exception as e:
                logger.error(f"Failed to read file: {str(e)}", exc_info=True)
                raise InvalidFileError(f"Failed to read file: {str(e)}")

            # 2. Create or get category
            filename = os.path.basename(file_path)
            category_name = f"{original_filename}__{os.path.splitext(filename)[0]}"
            
            if Category.objects.filter(name=category_name).exists():
                raise CategoryExistsError(f"Category '{category_name}' already exists. Import rolled back.")
            
            category = Category.objects.create(
                name=category_name,
                description=f"Words imported from {filename}"
            )
            logger.info(f"Created category: {category_name}")

            # 3. Process CSV
            csv_content = io.StringIO(content)
            reader = csv.reader(csv_content, delimiter=delimiter)
            
            for line_num, row in enumerate(reader, 1):

                # !!!!!!!!!!!!!!!!!!!
                # !!!!!!!!!!!!!!!!!!!
                # !!!!!!!!!!!!!!!!!!!
                time.sleep(1)

                stats['processed'] += 1
                
                # Skip empty rows
                if not row:
                    stats['skipped_empty'] += 1
                    continue
                
                # Parse row
                translation = row[0].strip() if len(row) > 0 else ''
                english = row[1].strip() if len(row) > 1 else ''
                description = row[2].strip() if len(row) > 2 else ''
                
                # Skip comments
                if translation and translation[0] in ('#', '-'):
                    stats['skipped_comments'] += 1
                    continue
                
                # Validate required fields
                if not english or not translation:
                    stats['skipped_empty'] += 1
                    stats['errors'].append(f'Line {line_num}: Missing word or translation')
                    continue
                
                # Create word
                try:
                    Word.objects.create(
                        word=english,
                        translation=translation,
                        user=user,
                        category=category,
                        description=description
                    )
                    stats['created'] += 1
                    
                    # Progress update for Flower
                    if stats['created'] % 100 == 0:
                        self.update_state(
                            state='PROGRESS',
                            meta={'created': stats['created'], 'processed': stats['processed']}
                        )
                        
                except Exception as e:
                    stats['errors'].append(f'Line {line_num}: {str(e)}')

            # 4. Validate results
            if stats['created'] == 0:
                raise NoWordsCreatedError(
                    f"No new words were created. "
                    f"Processed: {stats['processed']}, "
                    f"Skipped: {stats['skipped_empty'] + stats['skipped_comments']}"
                )

            # 5. Success response
            logger.info(f"Imported {stats['created']} words into {category_name}")
            return {
                'status': 'success',
                'message': f'Successfully imported {stats["created"]} words',
                'created': stats['created'],
                'errors': stats['errors'],
                'total_lines': stats['processed'],
                'category': category_name,
                'category_id': category.id
            }

    except (CategoryExistsError, NoWordsCreatedError, InvalidFileError) as e:
        # Expected failures - rollback automatically
        logger.warning(f"⚠️ Task rolled back: {str(e)}")
        
        # Update state for Flower
        self.update_state(
            state='FAILURE',
            meta={
                'message': str(e),
                'errors': stats['errors'][:10] if stats['errors'] else [],
                'stats': stats
            }
        )


        # FOR testing with EMPTY file
        # raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    
        # Пробрасываем исключение - задача становится FAILURE
        raise    

    except Exception as e:
        # Unexpected errors - retry with exponential backoff
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        
        # Update state for Flower
        self.update_state(
            state='RETRY',
            meta={
                'exc_message': str(e),
                'attempt': self.request.retries + 1,
                'max_retries': self.max_retries
            }
        )
        
        # Raise to trigger retry
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))