from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Student, Attendance
from .forms import AddStudent
from django.db.models import Count
from django.utils import timezone
import datetime
from django.contrib import messages
from .forms import AttendanceDateForm

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
        form.fields['roll_no'].disabled = True

    return render(request, 'students/edit_student.html', {'add_student': form, 'student': student})

def delete_student(request, username):
    student = get_object_or_404(Student, username=username)

    if request.method == "POST":
        student.delete()
        return redirect('student_list')

    return render(request, 'students/delete_student.html', {'student': student})


def dashboard(request):
    students = Student.objects.all()
    total_students = students.count()

    recent_students = students.order_by('-admission_date')[:5]

    by_class = (
        students.values('class_name')
        .annotate(count=Count('username'))
        .order_by('-count')
    )

    context = {
        'total_students': total_students,
        'recent_students': recent_students,
        'by_class': by_class,  # [{'class_name': 'BS CS', 'count': 45}, ...]
    }
    return render(request, 'students/dashboard.html', context)


def mark_attendance(request):
    selected_date = request.GET.get('date') or request.POST.get('date') or timezone.now().date().isoformat()
    students = Student.objects.all().order_by('roll_no')

    # Pull existing records for this date so the form pre-fills if you're re-opening it
    existing = {
        a.student_id: a.status
        for a in Attendance.objects.filter(date=selected_date)
    }

    if request.method == "POST":
        for student in students:
            status = request.POST.get(f"status_{student.username}")
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={"status": status}
                )
        messages.success(request, f"Attendance saved for {selected_date}.")
        return redirect(f"/attendance/mark/?date={selected_date}")

    context = {
        'students': students,
        'selected_date': selected_date,
        'existing': existing,
    }
    return render(request, 'students/mark_attendance.html', context)