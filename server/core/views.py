from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from celery.result import AsyncResult
from django_celery_results.models import TaskResult



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_status(request, task_id):
    """
    Check the status of import task
    """        
    task = AsyncResult(task_id)

    task_exists = TaskResult.objects.filter(task_id=task_id).exists()
    
    error_msg = str(task.info) if task.info else 'None'
    result = task.result or {}
    meta = task.info or {}
    
    print(f"📊 Task {task_id} - State: {task.state}")
    print(f"❌ Error: {error_msg}")
    print(f"📦 Result: {result}")
    print(f"📦 info: {meta}")
    print(f"💾 Exists in DB: {task_exists}")
    
    # Use task.state instead of task.pending
    if task.state == 'PENDING':
        response = {
            'status': 'pending', 
            'progress': 0,
        }
    elif task.state == 'FAILURE':
        response = {
            'status': 'failed',
            'error': str(task.info),
            'progress': 0,
            'message': f'Task failed: {str(task.info)}'
        }
    elif task.state == 'SUCCESS':
        result = task.result or {}
        response = {
            'status': 'completed',
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
        response = {
            'status': 'processing',
            'progress': meta.get('progress', 0),
            'message': f'Task is in state: {task.state}',
            'meta': meta
        }
    
    return Response(response)