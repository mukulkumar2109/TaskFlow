from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Job(models.Model):
    JOB_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'), 
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ]

    JOB_TYPE_CHOICES = [
        ('email', 'Email Job'),
        ('report', 'Report Generation'),
        ('file_process', 'File Processing'),
        ('api_call', 'API Call'),
        ('data_processing', 'Data Processing')
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    description = models.TextField(blank=True)
    parameters = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES)
    priority = models.IntegerField(default=0)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"