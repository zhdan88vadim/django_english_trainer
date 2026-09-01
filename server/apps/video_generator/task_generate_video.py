from celery import shared_task

from server.apps.video_generator.services.generate_video_service import generate_video_from_lines
import os

OUTPUT_DIR = "./outputs"

@shared_task(bind=True)
def generate_video_task(self, lines, task_id):
    try:
        self.update_state(state='PROGRESS', meta={'task_id': task_id, 'progress': 0, "status": "Task started",})       
        out_path = os.path.join(OUTPUT_DIR, f"{task_id}.mp4")

        print("out_path", out_path)
        
        def progress_cb(p, msg='---'):
            self.update_state(state='PROGRESS', meta={'task_id': task_id, 'progress': p, 'status': msg,})             

        generate_video_from_lines(lines, out_path, progress_cb=progress_cb)
        return {"out": out_path}
    except Exception as e:
        raise