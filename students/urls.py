from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Dashboard, name='Dashboard'),
    path('allstudents/', views.student_list, name='student_list'),
    path('addstudent/', views.add_student, name='add_student'),
    path('studentsuccess', views.success, name='student_success'),
]