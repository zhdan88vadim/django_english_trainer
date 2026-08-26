# tasks.py
from celery import shared_task
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.db import transaction
from .models import Word, Category
import csv
import io
import os

@shared_task
def import_words_from_csv(file_path, user_id, delimiter=';'):
    """
    Import CSV with rollback if no new words are created
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {'status': 'error', 'message': f'User {user_id} not found'}

    with transaction.atomic():
        try:
            filename = os.path.basename(file_path)
            category_name = os.path.splitext(filename)[0]

            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'discription': f"Words imported from {filename}"}
            )

            with default_storage.open(file_path, 'r') as file:
                content = file.read()
            
            csv_content = io.StringIO(content)
            reader = csv.reader(csv_content, delimiter=delimiter)
            
            created_count = 0
            errors = []
            
            for line_num, row in enumerate(reader, 1):
                if not row or len(row) < 2:
                    errors.append(f'Line {line_num}: Invalid format - row has {len(row)} columns')
                    continue
                
                translation = row[0].strip()
                english = row[1].strip()
                
                if not english or not translation:
                    errors.append(f'Line {line_num}: Empty word or translation')
                    continue
                
                try:
                    word, created = Word.objects.get_or_create(
                        word=english,
                        user=user,
                        defaults={
                            'word': english,
                            'translation': translation,
                            'user': user,
                            'category': category
                        }
                    )
                    
                    if created:
                        created_count += 1
                        
                except Exception as e:
                    errors.append(f'Line {line_num}: Database error - {str(e)}')

            # Rollback if no new words were created
            if created_count == 0:
                # This raises an exception to trigger rollback
                raise Exception("No new words were created. Rolling back...")
            
            return {
                'status': 'success',
                'created': created_count,
                'errors': errors,
                'total_lines': created_count + len(errors)
            }
            
        except Exception as e:
            # Transaction automatically rolls back
            return {
                'status': 'rolled_back',
                'message': str(e),
                'created': 0,
                'errors': errors if 'errors' in locals() else []
            }