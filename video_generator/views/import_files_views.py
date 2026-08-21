# views.py - Updated to handle multiple files and additional parameters

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..tasks import import_words_from_file, import_words_from_csv
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
    file_type = request.POST.get('file_type', 'txt')  # txt or csv
    
    # Save file temporarily
    file_extension = os.path.splitext(uploaded_file.name)[1]
    file_name = f"import_{uuid.uuid4()}{file_extension}"
    file_path = default_storage.save(file_name, ContentFile(uploaded_file.read()))
    
    # Start Celery task based on file type
    if file_type == 'csv':
        task = import_words_from_csv.delay(file_path, request.user.id, delimiter)
    else:
        task = import_words_from_file.delay(file_path, request.user.id, delimiter)
    
    return Response({
        'status': 'processing',
        'task_id': task.id,
        'file_path': file_path,
        'original_filename': uploaded_file.name,
        'message': 'File uploaded and import started.'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_multiple_files(request):
    """
    Upload multiple files at once
    """
    files = request.FILES.getlist('files')
    if not files:
        return Response({'error': 'No files uploaded'}, status=400)
    
    tasks = []
    for uploaded_file in files:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        file_name = f"import_{uuid.uuid4()}{file_extension}"
        file_path = default_storage.save(file_name, ContentFile(uploaded_file.read()))
        
        task = import_words_from_file.delay(file_path, request.user.id)
        tasks.append({
            'original_filename': uploaded_file.name,
            'task_id': task.id,
            'file_path': file_path
        })
    
    return Response({
        'status': 'processing',
        'total_files': len(files),
        'tasks': tasks,
        'message': 'All files queued for import.'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_status(request, task_id):
    """
    Check the status of import task
    """
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    if task.pending:
        response = {'status': 'pending', 'state': 'PENDING'}
    elif task.failed():
        response = {
            'status': 'failed',
            'state': 'FAILURE',
            'error': str(task.info)
        }
    elif task.successful():
        response = {
            'status': 'completed',
            'state': 'SUCCESS',
            'result': task.result
        }
    else:
        response = {
            'status': 'unknown',
            'state': task.state
        }
    
    return Response(response)