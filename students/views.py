from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Student, Attendance, Course
from .forms import AddStudent, AddCourse
from django.db.models import Count
from django.utils import timezone
import datetime
from django.contrib import messages
from .forms import AttendanceDateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth
from django.db.models import Q, Count

# Create your views here.
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def add_student(request):
    if request.method == "POST":
        form = AddStudent(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("student_success")
    else:
        form = AddStudent()  
    
    return render(request, 'students/add_student.html', {'add_student': form})      

@login_required
def success(request):
    return render(request, 'students/student_success.html')

@login_required
def student_profile(request, username):
    student = get_object_or_404(Student, username=username)
    attendance_history = student.attendances.all()[:15]  # most recent 15, thanks to Meta.ordering
    return render(request, 'students/student_profile.html', {
        'student': student,
        'attendance_history': attendance_history,
    })

@login_required
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

@login_required
def delete_student(request, username):
    student = get_object_or_404(Student, username=username)

    if request.method == "POST":
        student.delete()
        return redirect('student_list')

    return render(request, 'students/delete_student.html', {'student': student})



@login_required
def dashboard(request):
    students = Student.objects.all()
    total_students = students.count()
    recent_students = students.order_by('-admission_date')[:5]

    # Donut: group by class_name (always populated)
    by_class = (
        students.exclude(class_name__exact='')
        .values('class_name')
        .annotate(count=Count('username'))
        .order_by('-count')
    )

    total_courses = Course.objects.count()

    total_records = Attendance.objects.count()
    present_records = Attendance.objects.filter(status="Present").count()
    attendance_rate = round((present_records / total_records) * 100, 1) if total_records else None

    today = timezone.now().date().replace(day=1)
    months = [today - relativedelta(months=i) for i in range(5, -1, -1)]

    monthly_counts = (
        students.filter(admission_date__gte=months[0])
        .annotate(month=TruncMonth('admission_date'))
        .values('month')
        .annotate(count=Count('username'))
    )
    counts_by_month = {m['month'].strftime('%Y-%m'): m['count'] for m in monthly_counts}

    enrollment_labels = [m.strftime('%b') for m in months]
    enrollment_data = [counts_by_month.get(m.strftime('%Y-%m'), 0) for m in months]

    context = {
        'total_students': total_students,
        'recent_students': recent_students,
        'by_class': by_class,
        'total_courses': total_courses,
        'attendance_rate': attendance_rate,
        'enrollment_labels': enrollment_labels,
        'enrollment_data': enrollment_data,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def mark_attendance(request):
    selected_date = request.GET.get('date') or request.POST.get('date') or timezone.now().date().isoformat()
    students = Student.objects.all().order_by('roll_no')

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
        return redirect(f"{reverse('mark_attendance')}?date={selected_date}")

    context = {
        'students': students,
        'selected_date': selected_date,
        'existing': existing,
    }
    return render(request, 'students/mark_attendance.html', context)

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'students/course_list.html', {'courses': courses})

@login_required
def add_course(request):
    if request.method == "POST":
        form = AddCourse(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = AddCourse()
    return render(request, 'students/add_course.html', {'add_course': form})

@login_required
def reports_home(request):
    return render(request, 'students/reports_home.html')

@login_required
def student_report(request):
    students = Student.objects.all()

    course_id = request.GET.get('course')
    gender = request.GET.get('gender')

    if course_id:
        students = students.filter(course_id=course_id)
    if gender:
        students = students.filter(gender=gender)

    total = students.count()

    gender_breakdown = (
        students.values('gender')
        .annotate(count=Count('username'))
        .order_by('gender')
    )

    course_breakdown = (
        students.exclude(course__isnull=True)
        .values('course__name')
        .annotate(count=Count('username'))
        .order_by('-count')
    )

    context = {
        'students': students.order_by('name'),
        'total': total,
        'gender_breakdown': gender_breakdown,
        'course_breakdown': course_breakdown,
        'courses': Course.objects.all(),
        'selected_course': course_id,
        'selected_gender': gender,
    }
    return render(request, 'students/student_report.html', context)
