from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
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