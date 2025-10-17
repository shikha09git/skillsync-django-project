from django import forms 
from  django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

from .models import Course

class registerForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','description']
        