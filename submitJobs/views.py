from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from django.contrib.auth.models import User
from .tasks import process_job

def home(request):
    data = {"Hello, world. I'm Mukul."}
    return HttpResponse(data)



@api_view(['POST'])
def submit_job(request):
    try:
        name = request.data.get('name')
        job_type = request.data.get('type')
        description = request.data.get('description', '')
        parameters = request.data.get('parameters', {})
        
        if not name or not job_type:
            return Response({"error": "Missing required fields: name or type."}, status=status.HTTP_400_BAD_REQUEST)
        
        created_by = User.objects.first()

        job = Job.objects.create(
            name = name,
            type = job_type,
            description = description,
            parameters = parameters,
            created_by = created_by
        )

        process_job.delay(job.id)

        return Response(
            {
                "message": "Job submitted successfully!",
                "job_id": job.id,
                "name": job.name,
                "type": job.type,
                "status": job.status
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)