from celery import shared_task
import time
from .models import Job

@shared_task
def process_job(job_id):
    job = None
    try:
        job = Job.objects.get(id=job_id)
        job.status = "running"
        job.save()
        print(f"processing job: {job.name} ({job.type})")
    
        if job.type == "report":
            time.sleep(5)
            job.result = "Report generated"
        elif job.type == "email":
            time.sleep(5)
            job.result = "Email sent"
        elif job.type == "data_processing":
            time.sleep(5)
            job.result = "Data processed"
        else:
            job.result = "Unknown job"

        job.status = "completed"
        job.save()
        print(f"Job {job_id} completed.")
        return f"Job {job_id} finished successfully!"
    
    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        job.status = "failed"
        job.result = str(e)
        job.save()

@shared_task
def test_task():
    print("celery is working fine.")
    time.sleep(5)
    print("test task completed.")
    return "done"