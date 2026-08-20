from django.shortcuts import render
from .models import Student
# Create your views here.

def Dashboard(request):
    return render(request, 'students/Dashboard.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})
