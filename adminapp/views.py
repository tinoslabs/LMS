from django.contrib.auth import authenticate, login,logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from testapp.models import User

from django.contrib import messages
from testapp.forms import UserRegistrationForm

from testapp.models import Categories,Course,Level,Video,Categoriestheory,Author,Language,What_u_learn,Requirements,Lesson,VideoModel,Instructor
from testapp.forms import CategoryForm,AuthorForm,LevelForm,LanguageForm,CourseForm,CategoriestheoryForm,WhatULearnForm,RequirementsForm,LessonForm,VideoForm,VideosForm,PasswordChangeForm,InstructorForm
# from .settings import *

from django.shortcuts import get_object_or_404, redirect,render

from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
# import razorpay
from time import time
from testapp.models import UserCourse,Payment

@user_passes_test(lambda u: u.is_superuser)  
def admin_approval_view(request):
    # Fetch all instructors
    instructors = User.objects.filter(role='instructor', is_approved=False)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')  # 'approve' or 'reject'
        user = get_object_or_404(User, id=user_id)

        if action == 'approve':
            user.is_approved = True
            user.save()
            messages.success(request, f'{user.username} has been approved.')
        elif action == 'reject':
            # Optional: Handle rejection (you can also delete or deactivate the user)
            messages.error(request, f'{user.username} has been rejected.')

        return redirect('admin_approval')

    return render(request, 'admin/admin_approval.html', {'instructors': instructors})

def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def instructor_list(request):
    instructors = User.objects.filter(role='instructor')
    return render(request, 'admin/instructor_list.html', {
        'instructors': instructors
    })

def student_list(request):
    students = User.objects.filter(role='student')
    return render(request, 'admin/student_list.html', {
        'students': students
    })    

