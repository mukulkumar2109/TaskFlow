from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Job
from .serializers import JobSerializer
from django.shortcuts import get_object_or_404
from .tasks import queue, execute_job
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.storage import default_storage
from .tasks import queue, data_cleanup_real

class DataCleanupJobView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save file temporarily
        file_path = default_storage.save(f'uploads/{file_obj.name}', file_obj)

        # Create a Job entry
        job = Job.objects.create(
            name="Data Cleanup Job",
            description="Cleans CSV data and returns cleaned file",
            owner=request.user if request.user.is_authenticated else None,
            input_file=file_path,
            status="queued"
        )

        # Queue the job in Redis
        queue.enqueue(data_cleanup_real, file_path, str(job.id))

        return Response({
            "message": "Data cleanup job submitted successfully!",
            "job_id": job.id,
            "input_file": f"{settings.MEDIA_URL}{file_path}"
        }, status=status.HTTP_201_CREATED)


# List all jobs or create a new one
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    def perform_create(self, serializer):
        job = serializer.save()
        # enqueue background execution
        queue.enqueue(execute_job, job.name)


# Retrieve, update, or delete a specific job
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'

# Simple health check endpoint
class HealthCheckView(APIView):
    def get(self, request):
        return Response({"message": "Backend is connected successfully!"}, status=status.HTTP_200_OK)
