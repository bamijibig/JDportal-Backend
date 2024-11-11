from django.db import models


class Staff(models.Model):
    staffid = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20)
    staffid = models.CharField(max_length=20, blank=True, null=True)
    division = models.CharField(max_length=100)
    dept = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bhub = models.CharField(max_length=100, blank=True, null=True)
    scenter = models.CharField(max_length=100, blank=True, null=True)
    office_addr = models.CharField(max_length=255, default="Not Set")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.firstname} {self.surname}"

# models.py
# from django.db import models
from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Job(models.Model): 
    job_title = models.CharField(max_length=100)
    job_div = models.ForeignKey(Division, on_delete=models.CASCADE)
    is_mgr = models.BooleanField(default=False)
    reports_to = models.CharField(max_length=100)
    jd_file = models.FileField(upload_to='JD_Files/', blank=True, null=True)
    kpi_file = models.FileField(upload_to='KPI_Files/', blank=True, null=True)
    tracker_file = models.FileField(upload_to='Tracker_Files/', blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return self.job_title
# KPI List model that stores extracted KPIs for a job title
class KPI(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # Link KPI list to a job title
    kpis = models.TextField()  # Store the KPI descriptions
    weight = models.CharField(max_length=500, default='0')  # Store weight as a string (e.g., '20 || 20 || 15 || 20')
    status = models.BooleanField(default=True)  # Use Boolean to represent active/inactive status

    def __str__(self):
        return f"KPI List for {self.job.job_title}"

# Appraisal model for evaluating staff based on their KPIs
# class Tracker(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_tracker')
#     kpi_list = models.ForeignKey(KPI, on_delete=models.CASCADE)  # KPIs related to the staff member's job title
#     score = models.DecimalField(max_digits=5, decimal_places=2)  # Score for the KPIs
#     comments = models.TextField(null=True, blank=True)
#     appraisal_date = models.DateField()

#     def __str__(self):
#         return f"Appraisal for {self.staff.full_name} on {self.appraisal_date}"

#     def calculate_total_weight(self):
#         # Assuming weights are stored as '20 || 20 || 15 || 20' and we need to calculate the total
#         weights = [int(w.strip()) for w in self.kpi_list.weight.split('||')]
#         return sum(weights)


class Region(models.Model):
    name= models.CharField(max_length=255)
    address=models.CharField(max_length=255)
class BusinessHub(models.Model):
    region=models.ForeignKey(Region, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    address=models.CharField(max_length=255)
class Scenter(models.Model):
    bhub=models.ForeignKey(BusinessHub, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    address=models.CharField(max_length=255)    
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
##########################################################################################################
# class Tracker(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     # kpi_item = models.TextField()
#     kpi_item=models.ManyToManyField(KPI, on_delete=models.CASCADE)
#     tr_month = models.CharField(max_length=2)
#     tr_year = models.CharField(max_length=4)
#     score = models.CharField(max_length=255)
#     comments = models.TextField()
#     created_by = models.ForeignKey(Staff, related_name='supervisor', on_delete=models.CASCADE)

# class TrackerComment(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     tr_month = models.CharField(max_length=2)
#     tr_year = models.CharField(max_length=4)
#     comments = models.TextField()
#     created_by = models.ForeignKey(Staff, related_name='supervisor', on_delete=models.CASCADE)
