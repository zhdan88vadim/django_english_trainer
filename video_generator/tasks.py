# tasks.py
from celery import shared_task
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from .models import Word
import csv
import io

@shared_task
def import_words_from_file(file_path, user_id, delimiter=';'):
    """
    Import words from a text file using Celery
    
    File format: English;Translation (one per line)
    Example: 
        How do we implement the Dependency Inversion Principle?;How do we implement the Dependency Inversion Principle?
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {'status': 'error', 'message': f'User {user_id} not found'}
    
    try:
        # Read file content
        with default_storage.open(file_path, 'r') as file:
            content = file.read()
        
        # Parse the content
        lines = content.strip().split('\n')
        created_count = 0
        errors = []
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
                
            # Split by delimiter
            parts = line.strip().split(delimiter)
            
            if len(parts) != 2:
                errors.append(f'Line {line_num}: Invalid format - expected 2 parts, got {len(parts)}')
                continue
            
            english, translation = parts[0].strip(), parts[1].strip()
            
            if not english or not translation:
                errors.append(f'Line {line_num}: Empty word or translation')
                continue
            
            try:
                # Check if word already exists for this user
                word, created = Word.objects.get_or_create(
                    word=english,
                    translation=translation,
                    user=user,
                    defaults={'word': english, 'translation': translation, 'user': user}
                )
                
                if created:
                    created_count += 1
                    
            except Exception as e:
                errors.append(f'Line {line_num}: Database error - {str(e)}')
        
        return {
            'status': 'success',
            'created': created_count,
            'errors': errors,
            'total_lines': len(lines)
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@shared_task
def import_words_from_csv(file_path, user_id, delimiter=';'):
    """
    Alternative CSV import with more control
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {'status': 'error', 'message': f'User {user_id} not found'}
    
    try:
        with default_storage.open(file_path, 'r') as file:
            content = file.read()
        
        # Use StringIO to parse CSV
        csv_content = io.StringIO(content)
        reader = csv.reader(csv_content, delimiter=delimiter)
        
        created_count = 0
        errors = []
        
        for line_num, row in enumerate(reader, 1):
            if not row or len(row) < 2:
                errors.append(f'Line {line_num}: Invalid format - row has {len(row)} columns')
                continue
            
            english = row[0].strip()
            translation = row[1].strip()
            
            if not english or not translation:
                errors.append(f'Line {line_num}: Empty word or translation')
                continue
            
            try:
                word, created = Word.objects.get_or_create(
                    word=english,
                    translation=translation,
                    user=user,
                    defaults={'word': english, 'translation': translation, 'user': user}
                )
                
                if created:
                    created_count += 1
                    
            except Exception as e:
                errors.append(f'Line {line_num}: Database error - {str(e)}')
        
        return {
            'status': 'success',
            'created': created_count,
            'errors': errors,
            'total_lines': created_count + len(errors)
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}