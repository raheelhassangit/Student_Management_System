from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="students/", blank=True, null=True)
    father_name = models.CharField(max_length=100)
    roll_no = models.IntegerField(null=False, unique=True)
    class_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),])    
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(max_length=200)
    admission_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Present")
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # one attendance record per student per day
        unique_together = ("student", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"    
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration_years = models.PositiveIntegerField(default=4)
    description = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"    