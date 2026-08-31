# views.py - Updated to handle multiple files and additional parameters

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from celery.result import AsyncResult

from ..task_import_words_from_csv import import_words_from_csv_task
import uuid
import os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_and_import_words(request):
    """
    Upload a text file and import words using Celery
    """
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({'error': 'No file uploaded'}, status=400)
    
    # Get optional parameters
    delimiter = request.POST.get('delimiter', ';')
        
    # Save file temporarily
    file_extension = os.path.splitext(uploaded_file.name)[1]
    file_name = f"import_{uuid.uuid4()}{file_extension}"
    file_path = default_storage.save(f'uploads/{file_name}', ContentFile(uploaded_file.read()))
    

    task = import_words_from_csv_task.delay(file_path, uploaded_file.name, request.user.id, delimiter)

    
    return Response({
        'status': 'processing',
        'task_id': task.id,
        'file_path': file_path,
        'original_filename': uploaded_file.name,
        'message': 'File uploaded and import started.'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_status(request, task_id):
    """
    Check the status of import task
    """        
    task = AsyncResult(task_id)

    from django_celery_results.models import TaskResult
    task_exists = TaskResult.objects.filter(task_id=task_id).exists()
    
    error_msg = str(task.info) if task.info else 'None'
    result = task.result or {}
    
    print(f"📊 Task {task_id} - State: {task.state}")
    print(f"❌ Error: {error_msg}")
    print(f"📦 Result: {result}")
    print(f"💾 Exists in DB: {task_exists}")
    
    # Use task.state instead of task.pending
    if task.state == 'PENDING':
        response = {
            'status': 'pending', 
            'state': 'PENDING',
            'progress': 0,
            'message': 'Task is pending'
        }
    elif task.state == 'FAILURE':
        response = {
            'status': 'failed',
            'state': 'FAILURE',
            'error': str(task.info),
            'progress': 0,
            'message': f'Task failed: {str(task.info)}'
        }
    elif task.state == 'SUCCESS':
        result = task.result or {}
        response = {
            'status': 'completed',
            'state': 'SUCCESS',
            'result': result,
            'progress': 100,
            'message': 'Task completed successfully'
        }
        # If result contains progress info, use it
        if isinstance(result, dict):
            if 'progress' in result:
                response['progress'] = result['progress']
            if 'message' in result:
                response['message'] = result['message']
    else:
        # Any other state (STARTED, RETRY, etc.)
        response = {
            'status': 'processing',
            'state': task.state,
            'progress': 50,  # Or calculate based on state
            'message': f'Task is in state: {task.state}'
        }
    
    return Response(response)