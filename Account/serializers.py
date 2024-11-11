
from rest_framework import serializers

from Account.models import KPI, Division, Job, Staff
# class JobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = ['id', 'job_title', 'job_div', 'is_mgr', 'reports_to', 'jd_file', 'kpi_file', 'tracker_file', 'status']

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"

# class KPISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KPI
#         fields = ['id', 'job', 'kpis', 'weights']


# Serializer for JobTitle model
class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields=['id','job_title','job_div','is_mgr','reports_to']

class JoballSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields="__all__"
        # fields = ['id', 'job_title', 'job_div',  'is_mgr', 'reports_to', 'jd_file', 'kpi_file', 'tracker_file', 'status']
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields="__all__"
# Serializer for KpiList model
class KpiListSerializer(serializers.ModelSerializer):
    job = JobTitleSerializer()  # Nesting the JobTitle Serializer to show job details

    class Meta:
        model = KPI
        fields = ['id', 'job', 'kpis', 'weight', 'status']
    
    # If you want to update the KPIs and weight fields with raw text rather than a nested job object,
    # you can modify the `create` and `update` methods.
    def create(self, validated_data):
        job_data = validated_data.pop('job')
        job = Job.objects.get(id=job_data['id'])
        kpi_list = KPI.objects.create(job=job, **validated_data)
        return kpi_list
    
    def update(self, instance, validated_data):
        job_data = validated_data.pop('job')
        job = Job.objects.get(id=job_data['id'])
        instance.job = job
        instance.kpis = validated_data.get('kpis', instance.kpis)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
