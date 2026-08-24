from django import forms
from .models import Student, Course


class AddStudent(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'username',
            'roll_no',
            'name',
            'father_name',
            'image',
            'address',
            'date_of_birth',
            'class_name',
            'gender',
            'phone',
            'email',
            'course',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class AttendanceDateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))        
    
class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'duration_years', 'description']    