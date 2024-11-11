import re
from rest_framework import viewsets
from Account.serializers import DivisionSerializer, StaffSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import KPI, Job, Division, Staff
from .serializers import JobSerializer, JobTitleSerializer, JoballSerializer
import pdfplumber
from django.core.files.storage import default_storage



import pdfplumber
from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from django.conf import settings
import os
# View for listing all jobs
class JobListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobTitleSerializer
# Create job view
class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobTitleSerializer

    def create(self, request, *args, **kwargs):
        job_title = request.data.get('job_title')
        job_div = request.data.get('job_div')
        reports_to = request.data.get('reports_to')
        is_mgr = bool(request.data.get('is_mgr'))

        try:
            job_div = Division.objects.get(name=job_div)
        except Division.DoesNotExist:
            return JsonResponse({"error": "Invalid division"}, status=400)

        Job.objects.create(
            job_title=job_title,
            job_div=job_div,
            reports_to=reports_to,
            is_mgr=is_mgr,
            status='Active'
        )
        return JsonResponse({"message": "Job created successfully"}, status=status.HTTP_201_CREATED)


# Retrieve, update, and upload files for a specific job
class JobDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JoballSerializer
    parser_classes = [MultiPartParser, FormParser]

    def retrieve(self, request, *args, **kwargs):
        job_id = kwargs.get('pk')
        try:
            job = Job.objects.get(id=job_id)
            job_data = {
                "job_id": job.id,
                "job_title": job.job_title,
                "job_division": job.job_div.name,
                "reports_to": job.reports_to if job.reports_to else None,
                "is_mgr": job.is_mgr,
                "status": job.status,
                "kpi_file": job.kpi_file.url if job.kpi_file else None,
                "jd_file": job.jd_file.url if job.jd_file else None,
                "tracker_file": job.tracker_file.url if job.tracker_file else None
            }
            return JsonResponse(job_data, safe=False, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)
    def post(self, request, *args, **kwargs):
        print("Post method called")
        job_id = kwargs.get('pk')
        
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)

        kpi_file = request.FILES.get('kpi_file')
        print("File received:", kpi_file)

        if not kpi_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Save file to 'media/uploads/'
        kpi_file_path = default_storage.save(f'uploads/{kpi_file.name}', kpi_file)
        print("File saved at:", kpi_file_path)

        # Convert relative path to absolute path
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, kpi_file_path)
        print("Absolute path for file processing:", absolute_file_path)

        # Extract KPI data using the absolute file path
        kpi_data = self.extract_kpi_data_from_pdf(absolute_file_path)
        print("KPI data extracted:", kpi_data)

        for kpi_item in kpi_data:
            # Ensure the 'weight' is a string, and handle as required
            weight = kpi_item.get('weight', '0')  # Default to '0' if no weight is found
            
            KPI.objects.create(
                job=job,
                kpis=kpi_item['kpi'],  # Use 'kpis' field to store KPI description
                weight=weight  # Store the weight as a string
            )
            print(f"Saved KPI for job {job.id}: {kpi_item['kpi']}, Weight: {weight}")

        # Save the file to the job instance's kpi_file field
        job.kpi_file.save(kpi_file.name, kpi_file)
        job.save()

        return JsonResponse({"message": "Files uploaded and job updated successfully"}, status=status.HTTP_201_CREATED)
   
    def extract_kpi_data_from_pdf(self, file_path):
        kpi_data = []
        kpi_pattern = re.compile(r"(.*?)\s+(\d+)%")  # Adjust regex as needed to capture KPI and Weight

        try:
            with pdfplumber.open(file_path) as pdf:
                capture = False
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue

                    for line in text.splitlines():
                        if "JOB KEY PERFORMANCE INDICATORS(KPI)" in line:
                            capture = True
                            continue

                        if "BOOSTERS" in line or "ERODERS" in line:
                            capture = False
                            break

                        if capture:
                            match = kpi_pattern.search(line)
                            if match:
                                kpi_text = match.group(1).strip()
                                weight_text = match.group(3).strip()
                                kpi_data.append({
                                    'kpi': kpi_text,
                                    'weight': weight_text
                                })
                                print(f"Extracted KPI: {kpi_text}, Weight: {weight_text}")

            print("Total KPIs extracted:", len(kpi_data))
        except Exception as e:
            print("Error during KPI extraction:", str(e))
        return kpi_data
    
    
################################################################################################
################################################################################################






class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_mgr=1)
    serializer_class = JobSerializer