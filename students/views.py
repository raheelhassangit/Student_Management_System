from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
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

def edit_student(request, username):
    student = get_object_or_404(Student, username=username)

    if request.method == "POST":
        form = AddStudent(request.POST, request.FILES, instance=student)
        if form.is_valid():
            new_username = form.cleaned_data['username']

            # Check availability only if username was actually changed
            if new_username != username and Student.objects.filter(username=new_username).exists():
                form.add_error('username', 'This username is already taken. Please choose another.')
            else:
                if new_username != username:
                    # Renaming the primary key: force an INSERT of the new row, then delete the old one
                    with transaction.atomic():
                        form.instance._state.adding = True
                        form.save()
                        Student.objects.filter(username=username).delete()
                else:
                    form.save()

                return redirect('student_profile', username=new_username)
    else:
        form = AddStudent(instance=student)

    return render(request, 'students/edit_student.html', {'add_student': form, 'student': student})