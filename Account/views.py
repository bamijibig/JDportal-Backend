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



# import pdfplumber
# from django.core.files.storage import default_storage
# from django.http import JsonResponse
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
# from django.conf import settings
# import os
# # View for listing all jobs
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


# # Retrieve, update, and upload files for a specific job
# class JobDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JoballSerializer
#     parser_classes = [MultiPartParser, FormParser]

#     def retrieve(self, request, *args, **kwargs):
#         job_id = kwargs.get('pk')
#         try:
#             job = Job.objects.get(id=job_id)
#             job_data = {
#                 "job_id": job.id,
#                 "job_title": job.job_title,
#                 "job_division": job.job_div.name,
#                 "reports_to": job.reports_to if job.reports_to else None,
#                 "is_mgr": job.is_mgr,
#                 "status": job.status,
#                 "kpi_file": job.kpi_file.url if job.kpi_file else None,
#                 "jd_file": job.jd_file.url if job.jd_file else None,
#                 "tracker_file": job.tracker_file.url if job.tracker_file else None
#             }
#             return JsonResponse(job_data, safe=False, status=status.HTTP_200_OK)
#         except Job.DoesNotExist:
#             return JsonResponse({"error": "Job not found"}, status=404)
#     def post(self, request, *args, **kwargs):
#         print("Post method called")
#         job_id = kwargs.get('pk')
        
#         try:
#             job = Job.objects.get(id=job_id)
#         except Job.DoesNotExist:
#             return JsonResponse({"error": "Job not found"}, status=404)

#         kpi_file = request.FILES.get('kpi_file')
#         print("File received:", kpi_file)

#         if not kpi_file:
#             return JsonResponse({"error": "No file uploaded"}, status=400)

#         # Save file to 'media/uploads/'
#         kpi_file_path = default_storage.save(f'uploads/{kpi_file.name}', kpi_file)
#         print("File saved at:", kpi_file_path)

#         # Convert relative path to absolute path
#         absolute_file_path = os.path.join(settings.MEDIA_ROOT, kpi_file_path)
#         print("Absolute path for file processing:", absolute_file_path)

#         # Extract KPI data using the absolute file path
#         kpi_data = self.extract_kpi_data_from_pdf(absolute_file_path)
#         print("KPI data extracted:", kpi_data)

#         for kpi_item in kpi_data:
#             # Ensure the 'weight' is a string, and handle as required
#             weight = kpi_item.get('weight', '0')  # Default to '0' if no weight is found
            
#             KPI.objects.create(
#                 job=job,
#                 kpis=kpi_item['kpi'],  # Use 'kpis' field to store KPI description
#                 weight=weight  # Store the weight as a string
#             )
#             print(f"Saved KPI for job {job.id}: {kpi_item['kpi']}, Weight: {weight}")

#         # Save the file to the job instance's kpi_file field
#         job.kpi_file.save(kpi_file.name, kpi_file)
#         job.save()

#         return JsonResponse({"message": "Files uploaded and job updated successfully"}, status=status.HTTP_201_CREATED)
       

#     def extract_kpi_data_from_pdf(self, file_path):
#         kpi_data = []
#         capture = False
#         kpi_description = ""

#         # Regular expression to capture only weight values (percentage values)
#         weight_pattern = re.compile(r"\b(\d+)%")
        
#         # Regular expression to detect sub-items (e.g., "a.", "b.", "c.") at the start of a line
#         sub_item_pattern = re.compile(r"^[a-zA-Z]\.\s")

#         try:
#             with pdfplumber.open(file_path) as pdf:
#                 for page in pdf.pages:
#                     text = page.extract_text()
#                     if not text:
#                         continue

#                     # Split the page text into lines for line-by-line processing
#                     for line in text.splitlines():
#                         # Start capturing after the KPI header
#                         if "JOB KEY PERFORMANCE INDICATORS(KPI)" in line:
#                             capture = True
#                             continue
#                         elif "BOOSTERS" in line or "ERODERS" in line:  # Stop capture before other sections
#                             capture = False
#                             break

#                         if capture:
#                             # Clean and merge lines if necessary
#                             line = line.strip()

#                             # Check if the line is part of a sub-item (e.g., a., b., c.)
#                             if sub_item_pattern.match(line) or not weight_pattern.search(line):
#                                 # Accumulate the line into the current KPI description
#                                 if kpi_description:
#                                     kpi_description += " " + line
#                                 else:
#                                     kpi_description = line
#                             else:
#                                 # A line with weight indicates the end of the current KPI
#                                 weight_match = weight_pattern.search(line)
#                                 if weight_match:
#                                     weight = weight_match.group(0)
#                                     kpi_data.append({
#                                         'kpi': kpi_description.strip(),
#                                         'weight': weight
#                                     })
#                                     # Reset the description for the next KPI
#                                     kpi_description = ""

#         except Exception as e:
#             print("Error during KPI extraction:", str(e))

#         print("Total KPIs extracted:", len(kpi_data))
#         return kpi_data


    
################################################################################################
################################################################################################

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Job, KPI
from .serializers import JoballSerializer
import os
import json

class JobDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JoballSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        job_id = kwargs.get('pk')
        
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)

        kpi_file = request.FILES.get('kpi_file')
        extracted_data = request.data.get('extracted_data')
        
        if not kpi_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Save file to 'media/uploads/'
        kpi_file_path = default_storage.save(f'uploads/{kpi_file.name}', kpi_file)

        # Save the uploaded file to the Job instance
        job.kpi_file.save(kpi_file.name, kpi_file)
        job.save()

        # Debugging - Print the extracted data received
        print("Extracted Data Received:", extracted_data)

        # If KPI data is available, parse and save to the database
        if extracted_data:
            try:
                # Parse JSON string into a Python list
                kpi_data = json.loads(extracted_data)
                print("Parsed KPI Data:", kpi_data)  # Debugging

                # Iterate through each extracted KPI and weight data
                for kpi_item in kpi_data:
                    print(f"Saving KPI Item: {kpi_item}")  # Debugging

                    # Ensure KPI and weight are present before saving
                    if 'kpi' in kpi_item and 'weight' in kpi_item:
                        weight = kpi_item.get('weight', '0')  # Default to '0' if missing
                        
                        KPI.objects.create(
                            job=job,
                            kpis=kpi_item['kpi'],  # Ensure this key exists
                            weight=weight  # Ensure this key exists
                        )
                    else:
                        print("Missing KPI or weight data in:", kpi_item)
                        return JsonResponse({"error": "Invalid KPI data structure"}, status=400)

            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return JsonResponse({"error": f"Error parsing KPI data: {str(e)}"}, status=400)

        return JsonResponse({"message": "Files uploaded and job updated successfully"}, status=status.HTTP_201_CREATED)





class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_mgr=1)
    serializer_class = JobSerializer