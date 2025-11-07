from django.db import models
from django.contrib.auth.models import User
import uuid

class Job(models.Model):
    JOB_STATUS = [
        ('created', 'Created'),
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('failed', 'Failed'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='created')
    schedule = models.CharField(max_length=100, blank=True, null=True)  # for cron-like scheduling
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    input_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    output_file = models.FileField(upload_to='cleaned_files/', null=True, blank=True)

    def __str__(self):
        return self.name


class JobRun(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='runs')
    run_id = models.UUIDField(default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default='running')
    logs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Run {self.run_id} for {self.job.name}"


class JobEvent(models.Model):
    job_run = models.ForeignKey(JobRun, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)
    event_payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event: {self.event_type} ({self.created_at})"
