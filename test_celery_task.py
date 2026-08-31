#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.settings')
django.setup()

from server.apps.video_generator.task_import_words_from_csv import import_words_from_file
from django.contrib.auth.models import User

# Test the task directly
def test_task():
    try:
        # Get a user
        user = User.objects.first()
        if not user:
            print("❌ No user found in database")
            return
        
        print(f"✅ Using user: {user.username} (ID: {user.id})")
        
        # Test file path
        file_path = "./oop.txt"
        
        # Call the task directly (synchronously for testing)
        print(f"📤 Testing import from: {file_path}")
        result = import_words_from_file.delay(file_path, user.id, ';')
        
        print("=" * 50)
        print("RESULT:")
        print("=" * 50)
        print(result)
        
        if result.get('status') == 'success':
            print(f"✅ Created {result.get('created', 0)} words")
            if result.get('errors'):
                print(f"⚠️  Errors: {len(result.get('errors', []))}")
                for error in result.get('errors', [])[:5]:
                    print(f"  - {error}")
        else:
            print(f"❌ Error: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_task()