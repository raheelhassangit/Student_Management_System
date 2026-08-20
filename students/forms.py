from django import forms
from .models import Student


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
        ]