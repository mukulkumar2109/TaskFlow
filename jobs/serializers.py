from rest_framework import serializers
from .models import Job, JobRun, JobEvent

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRun
        fields = '__all__'

class JobEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobEvent
        fields = '__all__'
