from django.shortcuts import render , redirect
from django.contrib.auth import login ,logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import registerForm , CourseForm
from .models import Course
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()  # <-- this line actually saves the user
            return redirect('login')
    else:
        form = registerForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password =request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})


