from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
