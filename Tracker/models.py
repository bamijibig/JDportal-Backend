from django.db import models

from Account.models import KPI, Staff
class Tracker(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)  # The staff being evaluated
    kpi_items = models.ManyToManyField(KPI)  # Multiple KPIs for one staff
    tr_month = models.CharField(max_length=2)  # Tracking the month of the evaluation
    tr_year = models.CharField(max_length=4)  # Tracking the year of the evaluation
    score = models.CharField(max_length=255)  # Score for the evaluation
    comments = models.TextField(blank=True)  # Comments by the evaluator  
    created_by = models.ForeignKey(Staff, related_name='supervisor', on_delete=models.CASCADE)  # The supervisor evaluating the staff
    # created_at=models.DateTimeField()
    def __str__(self):
        return f"Appraisal for {self.staff.firstname} on {self.tr_month}"

    # def calculate_total_weight(self):
    #     # Assuming weights are stored as '20 || 20 || 15 || 20' and we need to calculate the total
    #     weights = [int(w.strip()) for w in self.kpi_list.weight.split('||')]
    #     return sum(weights)
