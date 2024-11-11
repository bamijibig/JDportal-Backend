# from django.db import models

# # Create your models here.
# # models.py
# from django.db import models

# class Job(models.Model):
#     job_title = models.CharField(max_length=255)
#     jd_file = models.FileField(upload_to='jobs/', null=True, blank=True)
#     kpi_file = models.FileField(upload_to='kpis/', null=True, blank=True)
#     tracker_file = models.FileField(upload_to='trackers/', null=True, blank=True)
#     status = models.CharField(max_length=50, default='Active')

# class Division(models.Model):
#     div_name = models.CharField(max_length=255)

# class Staff(models.Model):
#     staffid = models.CharField(max_length=50, null=True, blank=True)
#     email = models.EmailField(unique=True)
#     phone_no = models.CharField(max_length=15, null=True, blank=True)
#     division = models.CharField(max_length=255, null=True, blank=True)
#     dept = models.CharField(max_length=255, null=True, blank=True)
#     job = models.CharField(max_length=255, null=True, blank=True)
#     grade = models.CharField(max_length=50, null=True, blank=True)
#     location = models.CharField(max_length=255, null=True, blank=True)
#     active = models.BooleanField(default=True)

# class Document(models.Model):
#     doc_name = models.CharField(max_length=255)
#     doc_type = models.CharField(max_length=50)
#     jd_file = models.FileField(upload_to='docs/')

# class KPI(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE)
#     kpi_item = models.TextField()

# class Tracker(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     kpi_item = models.TextField()
#     tr_month = models.CharField(max_length=2)
#     tr_year = models.CharField(max_length=4)
#     score = models.CharField(max_length=255)

# class TrackerComment(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     tr_month = models.CharField(max_length=2)
#     tr_year = models.CharField(max_length=4)
#     comments = models.TextField()
#     created_by = models.ForeignKey(Staff, related_name='supervisor', on_delete=models.CASCADE)
