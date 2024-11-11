
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Staff, KPI, Tracker
from .serializers import TrackerSerializer

class TrackerCreateView(APIView):
    def post(self, request, staff_id):
        # Get the staff being evaluated
        staff = get_object_or_404(Staff, id=staff_id)
        
        # Get the supervisor from the Staff table (based on the logged-in user's email)
        try:
            supervisor = Staff.objects.get(email=request.user.email)
        except Staff.DoesNotExist:
            return Response({"error": "Supervisor not found in the Staff table."}, status=status.HTTP_400_BAD_REQUEST)

        # Get tr_month and tr_year from the request data
        tr_month = request.data.get('tr_month')
        tr_year = request.data.get('tr_year')

        if not tr_month or not tr_year:
            return Response({"error": "tr_month and tr_year are required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Tracker object
        tracker = Tracker.objects.create(
            staff=staff,
            tr_month=tr_month,
            tr_year=tr_year,
            score=request.data.get('score'),
            comments=request.data.get('comments'),
            created_by=supervisor  # Set the supervisor as created_by (Staff instance)
        )
        
        # Add the KPI items to the tracker (received as a list of KPI IDs)
        kpi_items = request.data.get('kpi_items', [])
        for kpi_item in kpi_items:
            # You can get the KPI either by its ID or name
            if 'id' in kpi_item:
                kpi = get_object_or_404(KPI, id=kpi_item['id'])
            elif 'name' in kpi_item:
                kpi = get_object_or_404(KPI, name=kpi_item['name'])
            else:
                return Response({"error": "KPI ID or name is required."}, status=status.HTTP_400_BAD_REQUEST)
            tracker.kpi_items.add(kpi)
        
        # Save the tracker to the database
        tracker.save()

        # Serialize the saved tracker object and return a response
        serializer = TrackerSerializer(tracker)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



