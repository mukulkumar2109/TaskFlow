from django.contrib import admin
from .models import Job, JobRun, JobEvent

admin.site.register(Job)
admin.site.register(JobRun)
admin.site.register(JobEvent)
