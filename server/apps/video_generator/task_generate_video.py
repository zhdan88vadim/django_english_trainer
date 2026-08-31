from celery import shared_task

from server.apps.video_generator.services.generate_video_service import generate_video_from_lines
import os

# CELERY_BROKER = os.getenv("CELERY_BROKER", "redis://redis:6379/0")
# celery = Celery("tasks", broker=CELERY_BROKER)
# r = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=6379, db=0, decode_responses=True)
OUTPUT_DIR = "./outputs"

def set_status(task_id, status, progress=0, message=None, output_path=None):
    payload = {"status": status, "progress": progress, "message": message or "", "output": output_path or ""}
    # r.set(f"task:{task_id}", json.dumps(payload))

@shared_task
def generate_video_task(lines, task_id):
    try:
        set_status(task_id, "queued", 0, "Task started")
        out_path = os.path.join(OUTPUT_DIR, f"{task_id}.mp4")

        print("out_path", out_path)
        
        def progress_cb(p, msg):
            set_status(task_id, "processing", p, msg, out_path if p>=100 else "")
        generate_video_from_lines(lines, out_path, progress_cb=progress_cb)
        set_status(task_id, "finished", 100, "Completed", out_path)
        return {"out": out_path}
    except Exception as e:
        set_status(task_id, "error", 0, str(e))
        raise