import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskflow_backend.settings')
django.setup()
import time, random, json, os
from redis import Redis
from rq import Queue
from django.core.mail import send_mail
from django.conf import settings 
import pandas as pd
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Job

# Redis Connection
redis_conn = Redis(host='127.0.0.1', port=6379)
queue = Queue('taskflow', connection=redis_conn)


def send_email_notifications():
    print("[TaskFlow] 📧 Starting Real Email Notification Job...")
    
    subject = "TaskFlow Notification"
    message = "Hello from TaskFlow! This is a test email sent from your distributed job system."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ["mukulkumarmehndiratta@gmail.com"]  # 👈 Change this to the email you want
    
    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"[TaskFlow] ✅ Email sent successfully to {recipient_list}")
        return f"Email sent to {recipient_list}"
    except Exception as e:
        print(f"[TaskFlow] ❌ Failed to send email: {e}")
        return f"Email failed: {e}"

def data_cleanup_real(file_path, job_id):
    print(f"[TaskFlow] 🧹 Starting real data cleanup for: {file_path}")
    try:
        input_full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # Read CSV
        df = pd.read_csv(input_full_path)

        # Basic cleaning steps
        print("[TaskFlow] 🔧 Removing duplicates...")
        df.drop_duplicates(inplace=True)

        print("[TaskFlow] 🩹 Filling missing values...")
        df.fillna(method='ffill', inplace=True)

        print("[TaskFlow] 🧾 Normalizing numeric columns...")
        for col in df.select_dtypes(include='number').columns:
            if df[col].std() != 0:
                df[col] = (df[col] - df[col].mean()) / df[col].std()

        # Save cleaned CSV
        output_filename = f"cleaned_{os.path.basename(file_path)}"
        output_path = f"cleaned_files/{output_filename}"
        output_full_path = os.path.join(settings.MEDIA_ROOT, output_path)

        os.makedirs(os.path.dirname(output_full_path), exist_ok=True)
        df.to_csv(output_full_path, index=False)

        print(f"[TaskFlow] ✅ Cleaned file saved at: {output_full_path}")

        # Update job in DB
        job = Job.objects.get(id=job_id)
        job.output_file = output_path
        job.status = "completed"
        job.save()

        return f"Data cleaned successfully. Saved at {output_path}"

    except Exception as e:
        print(f"[TaskFlow] ❌ Data cleanup failed: {e}")
        job = Job.objects.get(id=job_id)
        job.status = "failed"
        job.save()
        return f"Data cleanup failed: {e}"

def generate_report():
    print("[TaskFlow] 📊 Generating Report...")
    time.sleep(2)
    report_content = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sales": random.randint(1000, 5000),
        "users": random.randint(50, 200),
        "errors": random.randint(0, 5)
    }
    os.makedirs("reports", exist_ok=True)
    file_path = f"reports/report_{int(time.time())}.json"
    with open(file_path, "w") as f:
        json.dump(report_content, f, indent=4)
    print(f"[TaskFlow] ✅ Report generated at {file_path}")
    return f"Report created successfully: {file_path}"

def resize_images():
    print("[TaskFlow] 🖼️ Starting Image Resize Job...")
    time.sleep(5)
    print("[TaskFlow]  All images resized successfully!")
    return "Image resizing completed."

def train_dummy_ml_model():
    print("[TaskFlow] Starting Dummy ML Model Training...")
    for i in range(1, 6):
        print(f"[TaskFlow] Training progress: {i*20}%")
        time.sleep(1)
    print("[TaskFlow] Dummy ML model trained successfully!")
    return "Dummy ML training complete."


def execute_job(job_name):
    """
    Central dispatcher function called by Django when a new job is created.
    """
    job_name = job_name.lower().strip()

    if "email" in job_name:
        return send_email_notifications()
    elif "report" in job_name:
        return generate_report()
    elif "image" in job_name:
        return resize_images()
    elif "train" in job_name:
        return train_dummy_ml_model()
    else:
        print(f"[TaskFlow] ⚠️ Unknown job type: {job_name}")
        return f"No logic found for job '{job_name}'."
