from django.shortcuts import render , redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login ,logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import registerForm , contentForm
from .models import Content
from .models import Content, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    content = Content.objects.all().order_by('-created_at')  # fetch all Content
    return render(request, 'home.html', {'contents': content})

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
def add_content(request):
    if request.method == "POST":
        form = contentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.created_by = request.user
            content.save()
            return redirect('home')
    else:
        form = contentForm()
    return render(request, 'add_content.html', {'form': form})


@login_required
def like_content(request, course_id):
    course = get_object_or_404(Content, id=course_id)
    if request.user in course.likes.all():
        course.likes.remove(request.user)
        liked = False
    else:
        course.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': course.total_likes()})


@login_required
def add_comment(request, course_id):
    if request.method == 'POST':
        body = request.POST.get('body')
        course = get_object_or_404(Content, id=course_id)
        Comment.objects.create(course=course, user=request.user, body=body)
    return redirect('home')

@login_required
def delete_content(request, course_id):
    course = get_object_or_404(Content, id=course_id)

    # Only allow the creator to delete
    if course.created_by == request.user:
        course.delete()
        messages.success(request, "Course deleted successfully!")
    else:
        messages.error(request, "You are not allowed to delete this course.")

    return redirect('home')