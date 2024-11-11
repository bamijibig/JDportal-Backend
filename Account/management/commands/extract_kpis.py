import os
import pandas as pd
from django.core.management.base import BaseCommand
from Account.models import Job, KPI

class Command(BaseCommand):  # This is the Command class Django is looking for
    help = 'Extract KPIs from Excel files and populate the KpiList model'

    def handle(self, *args, **kwargs):
        # Find all job titles that have an associated KPI file
        jobs_with_kpi_files = Job.objects.exclude(kpi_file='')

        for job in jobs_with_kpi_files:
            kpi_file_path = job.kpi_file.path  # Get the file path for the KPI file

            # Check if the file exists
            if not os.path.exists(kpi_file_path):
                self.stdout.write(self.style.ERROR(f'File not found: {kpi_file_path}'))
                continue

            # Load the Excel file using pandas
            try:
                df = pd.read_excel(kpi_file_path, engine='openpyxl')
                print(df.columns)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error reading file: {kpi_file_path}, {str(e)}'))
                continue

            # Assuming the Excel file has columns 'KPIs' and 'Weights'
            kpis = df['EMPLOYEE MONTHLY KPI TRACKER 2023'].tolist()
            print(kpis)
            weights = df['Weights'].tolist()
            print(weights)

            # Convert lists to strings joined by ' || ' for storage in the database
            kpi_str = ' || '.join([str(kpi) for kpi in kpis])
            weight_str = ' || '.join([str(weight) for weight in weights])

            # Create or update the KpiList for the job
            kpi_list, created = KPI.objects.update_or_create(
                job=job,
                defaults={
                    'kpis': kpi_str,
                    'weight': weight_str,
                    'status': True  # Mark as active by default
                }
            )
            print(kpi_list)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created KPI list for {job.job_title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated KPI list for {job.job_title}'))

        self.stdout.write(self.style.SUCCESS('KPI extraction completed.'))




# import pandas as pd

# # Load Excel file
# file_path = '/mnt/data/Business_Application_Administrator.xlsx'
# xls = pd.ExcelFile(file_path)

# # Load the first sheet
# df = xls.parse(xls.sheet_names[0])

# def extract_kpis_and_core_values(df):
#     # Initialize empty lists for KPIs and Core Values
#     kpi_list = []
#     core_values_list = []
    
#     # Locate headers
#     kpi_header = 'Key Performance Indicators'
#     core_values_header = 'SECTION II – CORE VALUES'
    
#     # Variables to keep track of section start
#     extracting_kpis = False
#     extracting_core_values = False
    
#     for index, row in df.iterrows():
#         row_values = row.astype(str).str.strip().tolist()
#         if any(kpi_header in str(val) for val in row_values):
#             extracting_kpis = True
#             extracting_core_values = False
#             continue  # Skip header row
#         if any(core_values_header in str(val) for val in row_values):
#             extracting_core_values = True
#             extracting_kpis = False
#             continue  # Skip header row

#         # Extract KPIs
#         if extracting_kpis and row_values[0].strip().isdigit():  # Assuming KPIs start with a serial number
#             kpi_list.append({
#                 'KPI': row_values[1],  # The KPI description
#                 'Jan': row_values[2], 'Feb': row_values[3], 'Mar': row_values[4],
#                 'Apr': row_values[5], 'May': row_values[6], 'Jun': row_values[7],
#                 'Jul': row_values[8], 'Aug': row_values[9], 'Sep': row_values[10],
#                 'Oct': row_values[11], 'Nov': row_values[12], 'Dec': row_values[13],
#             })
        
#         # Extract Core Values
#         if extracting_core_values and row_values[0].strip().isdigit():  # Assuming Core Values also start with a serial number
#             core_values_list.append({
#                 'Core Value': row_values[1],  # The Core Value description
#                 'Jan': row_values[2], 'Feb': row_values[3], 'Mar': row_values[4],
#                 'Apr': row_values[5], 'May': row_values[6], 'Jun': row_values[7],
#                 'Jul': row_values[8], 'Aug': row_values[9], 'Sep': row_values[10],
#                 'Oct': row_values[11], 'Nov': row_values[12], 'Dec': row_values[13],
#             })

#     return kpi_list, core_values_list

# # Extract KPI and Core Values data
# kpis, core_values = extract_kpis_and_core_values(df)

# # Display extracted data
# print("Key Performance Indicators:")
# for kpi in kpis:
#     print(kpi)

# print("\nCore Values:")
# for core_value in core_values:
#     print(core_value)
