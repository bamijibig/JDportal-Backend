"""
URL configuration for JdPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from Account import views
from django.conf.urls.static import static

from JdPortal import settings 

router = routers.DefaultRouter()
# router.register(r'job',views.JobViewSet , basename='jobviewset')
router.register(r'div',views.DivisionViewSet , basename='divviewset')
router.register(r'staff',views.StaffViewSet , basename='staffviewset')
router.register(r'newjoblist',views.JobViewSet , basename='jobviewset')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Tracker.urls')),
    path('', include(router.urls)),
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('Tracker.urls')),
#     path('', include(router.urls)),
#     # path('upload-job/', views.JobCreateView.as_view(), name='upload-job'),
#     # path('upload-doc/{job_id}/', views.JobUploadFilesView.as_view(), name='upload-doc'),
#     # URL for listing all jobs
#     path('jobs/', views.JobListView.as_view(), name='job-list'),

#     # URL for creating a new job
#     path('jobs/create/', views.JobCreateView.as_view(), name='job-create'),

#     # URL for retrieving, updating, and uploading files for a specific job
#     path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    
    
    
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


