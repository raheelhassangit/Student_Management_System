from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import AddStudent
# Create your views here.

def Dashboard(request):
    return render(request, 'students/Dashboard.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def add_student(request):
    if request.method == "POST":
        form = AddStudent(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("student_success")
    else:
        form = AddStudent()  
    
    return render(request, 'students/add_student.html', {'add_student': form})      

def success(request):
    return render(request, 'students/student_success.html')

def student_profile(request, username):
    student = get_object_or_404(Student, username=username)
    return render(request, 'students/student_profile.html', {'student': student})