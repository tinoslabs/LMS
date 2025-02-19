from django.contrib.auth import authenticate, login,logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from testapp.models import User

from django.contrib import messages
from testapp.forms import UserRegistrationForm

from testapp.models import Certificate,Categories,Course,Level,Video,Categoriestheory,Author,Language,What_u_learn,Requirements,Lesson,VideoModel,Instructor
from testapp.forms import CategoryForm,AuthorForm,LevelForm,LanguageForm,CourseForm,CategoriestheoryForm,WhatULearnForm,RequirementsForm,LessonForm,VideoForm,VideosForm,PasswordChangeForm,InstructorForm
from .forms import UserForm_byAdmin
from lecturerapp.decorators import allowed_roles
from django.contrib import messages
from testapp.models import User, Instructor

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

def get_verified_quiz_results(request):
    # Step 1: Get the quiz for the given course (assuming there's one quiz per course)
    verified_quiz_results = Certificate.objects.filter(verified = True)

    return render(request, 'admin/quiz/verified_quiz_results.html', {'verified_quiz_results':verified_quiz_results} )


def upload_certificate(request, verified_quiz_result_id):
    if request.method == "POST" and 'certificate_file' in request.FILES:

        verified_quiz_result = get_object_or_404(Certificate, id = verified_quiz_result_id)
        
        verified_quiz_result.certificate_file = request.FILES['certificate_file']
        verified_quiz_result.uploaded_by = request.user
        verified_quiz_result.uploaded = True
        verified_quiz_result.save()
        messages.success(request, "Certificate successfully uploaded.")

        return redirect('verified_results') 
    else:
        messages.error(request, " Failed to Upload file...")
        return redirect('verified_results') 

def all_courses(request):
    courses = Course.objects.all()
    return render(request,'admin/all_courses.html',{'courses':courses})    

@login_required
@allowed_roles(['admin'])
def all_users_list(request):
    users = User.objects.all()
    return render(request,'admin/all_users_list.html',{'users':users})  


@login_required
def add_edit_user(request):

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form = UserForm_byAdmin(request.POST, instance=user)
        else:
            form = UserForm_byAdmin(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            if not user_id:
                user.set_password(form.cleaned_data["password1"])
            user.save()

            if user.role == "instructor":
                instructor_form = InstructorForm(request.POST)
                if instructor_form.is_valid():
                    instructor, created = Instructor.objects.get_or_create(user=user)
                    instructor.designation = instructor_form.cleaned_data["designation"]
                    instructor.about_author = instructor_form.cleaned_data["about_author"]
                    instructor.save()

            messages.success(request, "User saved successfully!")
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    return redirect('all_users_list')


@login_required
@allowed_roles(['admin'])
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        username = user.username  # Save for message
        user.delete()
        messages.success(request, f"User '{username}' has been deleted successfully!")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def user_management(request):
        return render(request,'admin/all_user_management.html')  
