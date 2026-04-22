from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from datetime import datetime

import PyPDF2
import docx
import json
import requests
import os
import time
import re

# 🔹 INDEX (redirect based on login)
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')


# 🔹 EMAIL LOGIN
def email_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'tasks/login.html')


# 🔹 LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# 🔹 HOME (Task Dashboard)
@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)

    # ✅ Add greeting logic
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning,"
    elif hour < 18:
        greeting = "Good Afternoon,"
    else:
        greeting = "Good Evening,"

    return render(request, 'tasks/home.html', {
        'tasks': tasks,
        'greeting': greeting   # ✅ IMPORTANT
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def task_page(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'tasks/tasks.html', {'tasks': tasks})


# ✅ AJAX ADD TASK
@csrf_exempt
@login_required
def add_task_ajax(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        task = Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date if due_date else None
        )

        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'due_date': str(task.due_date)
        })

# 🔹 DELETE TASK
@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('home')


# 🔹 TOGGLE COMPLETE
@login_required
def toggle_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('home')


# 🔹 SIGNUP 
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print("USERNAME:", username)  # 👈 DEBUG

        # 🚨 Check empty username
        if not username:
            messages.error(request, "Username is required")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username.strip(),  # ✅ important
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'tasks/signup.html')

# 🔹 FORGOT PASSWORD (dummy for now)
def forgot_password(request):
    return render(request, 'tasks/forgot.html')