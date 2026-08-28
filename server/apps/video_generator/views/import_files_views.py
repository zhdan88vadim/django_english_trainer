# views.py - Updated to handle multiple files and additional parameters

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..tasks import import_words_from_csv
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
    

    task = import_words_from_csv.delay(file_path, uploaded_file.name, request.user.id, delimiter)

    
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