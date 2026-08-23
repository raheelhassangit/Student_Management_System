from django.urls import path
from . import views 

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('allstudents/', views.student_list, name='student_list'),
    path('addstudent/', views.add_student, name='add_student'),
    path('studentsuccess', views.success, name='student_success'),
    path('student/<str:username>/', views.student_profile, name='student_profile'),
    path('student/<str:username>/edit/', views.edit_student, name='edit_student'),
    path('student/<str:username>/delete/', views.delete_student, name='delete_student'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
]