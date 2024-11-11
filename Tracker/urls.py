
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from Tracker import views

urlpatterns = [
    path('tracker/create/<int:staff_id>/',views.TrackerCreateView.as_view(), name='tracker-create'),
    
    
]
