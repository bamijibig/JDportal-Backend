from rest_framework import serializers

from Account.models import KPI, Division, Job
from .models import Tracker


class TrackerSerializer(serializers.ModelSerializer):
    kpi_items = serializers.PrimaryKeyRelatedField(many=True, queryset=KPI.objects.all())
    
    class Meta:
        model = Tracker
        fields = ['staff', 'kpi_items', 'tr_month', 'tr_year', 'score', 'comments', 'created_by']



# class JobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = ['id', 'job_title', 'job_div', 'is_mgr', 'reports_to', 'jd_file', 'kpi_file', 'tracker_file', 'status']

# class DivisionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Division
#         fields = ['id', 'name']

# class KPISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KPI
#         fields = ['id', 'job', 'kpis', 'weights']
