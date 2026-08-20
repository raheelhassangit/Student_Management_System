from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard, name='Dashboard'),
    path('allstudents/', views.view_students, name='allstudents')
]