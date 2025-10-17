from django import forms
from .models import Content
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Registration form
class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Content form
class contentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'instructor', 'duration']

