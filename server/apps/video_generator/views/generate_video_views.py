from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from server.apps.video_generator.task_generate_video import generate_video_task
from ..task_import_words_from_csv import import_words_from_csv_task
import uuid
import csv
import io
import os
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_video_from_csv_file(request: Request):
    """
    Upload a text file and import words using Celery
    """

    print("DATA:", request.data)

    text: str | None= request.data.get('text')
    if not text:
        return Response({'error': 'No text uploaded !! '}, status=400)

    lines = [
        line.strip() 
        for line in text.split('\n') 
        if line.strip() and not line.strip().startswith('#')
    ]    

    date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    task = generate_video_task.delay(lines, date_time)

    # uploaded_file = request.FILES.get('file')
    # if not uploaded_file:
    #     return Response({'error': 'No file uploaded'}, status=400)
        
    # # Save file temporarily
    # file_extension = os.path.splitext(uploaded_file.name)[1]
    # file_name = f"generate_video__{uuid.uuid4()}{file_extension}"
    # file_path = default_storage.save(f'uploads/{file_name}', ContentFile(uploaded_file.read()))

    # with default_storage.open(file_path, 'r') as file:
    #     lines = file.readlines()
    #     task = generate_video_task.delay(lines, file_name)

    
    return Response({
        'status': 'processing',
        'task_id': task.id,
        'file_path': date_time,
        'original_filename': date_time,
        'message': 'File uploaded and import started.'
    })
