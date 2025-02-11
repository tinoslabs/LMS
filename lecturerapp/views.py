from django.contrib.auth import authenticate, login,logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from .decorators import allowed_roles


from django.contrib import messages
from testapp.models import User

from django.contrib import messages
from testapp.forms import UserRegistrationForm

from testapp.models import Certificate,QuizResult,Quiz,Categories,Course,Level,Video,Categoriestheory,Author,CourseResource,Language,What_u_learn,Requirements,Lesson,VideoModel,Instructor
from testapp.forms import QuestionForm,QuizForm,CategoryForm,AuthorForm,LevelForm,LanguageForm,CourseForm,CourseResourceForm,CategoriestheoryForm,WhatULearnForm,RequirementsForm,LessonForm,VideoForm,VideosForm,PasswordChangeForm,InstructorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



def lecture_dashboard(request):
    return render(request,'lecture/lecture_dashboard.html')

def account(request):
    return render(request,'lecture/account.html')


# @login_required
# @allowed_roles()
# def lecture_profile(request):
#     if request.method == 'POST':
#         print("hiiiiiiii")
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('lecture_profile')  
#     else:
#         profile_form = UserProfileForm(instance=request.user)
#     return render(request, 'users/lecture_profile.html', {'profile_form': profile_form})

@login_required
@allowed_roles(['admin_and_instructor'])
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            category, created = Categories.objects.get_or_create(
                name=form.cleaned_data['name'],
                defaults={'icon': form.cleaned_data['icon']}
            )
            if created:
                messages.success(request, "Category added successfully!")
            else:
                messages.info(request, "Category already exists.")
            return redirect('category_list')
    else:
        form = CategoryForm()
        if request.user.role == 'instructor':
            template_name = 'lecture/add_category.html'
        else:
            template_name = 'admin/add_category.html'
    return render(request, template_name, {'form': form})


@login_required
@allowed_roles(['admin_and_instructor'])   #for restricting student
def category_list(request):
    categories = Categories.objects.all()
    if request.user.role == 'instructor':
        template_name = 'lecture/category_list.html'
    else:
        template_name = 'admin/category_list.html'
    
    return render(request, template_name, {'categories': categories})


@login_required
@allowed_roles(['admin_and_instructor'])
def update_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)  # Fetch the category object
    if request.method == 'POST':
        # Initialize the form with POST data, FILES, and bind it to the category instance
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()  # Save the updated data to the database
            messages.success(request, "Category updated successfully!")
            return redirect('category_list')
    else:
        # Pre-fill the form with the current category instance
        form = CategoryForm(instance=category)
        if request.user.role == 'instructor':
            template_name = 'lecture/update_category.html'
        else:
            template_name = 'admin/update_category.html'
    return render(request, template_name, {'form': form, 'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('category_list')

@login_required
def create_instructor(request):
    if request.method == 'POST':
        # Check if the logged-in user already has an Instructor profile
        if Instructor.objects.filter(user=request.user).exists():
            messages.error(request, "You already have an instructor profile.")
            return redirect('create_instructor')  # Replace with your desired page

        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            instructor = form.save(commit=False)
            instructor.user = request.user 
            instructor.save()
            messages.success(request, "Instructor profile created successfully!")
            return redirect('InstructorListView') 
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('create_instructor')
    else:
        form = InstructorForm()

    return render(request, 'lecture/instructor_form.html', {'form': form})


@login_required
def update_instructor(request):
    # Fetch the instructor profile of the logged-in user
    instructor = get_object_or_404(Instructor, user=request.user)

    if request.method == 'POST':
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor profile updated successfully!")
            return redirect('InstructorListView')  # Replace with your desired page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InstructorForm(instance=instructor)

    return render(request, 'lecture/update_instructor.html', {'form': form})


@login_required
def delete_instructor(request):
    # Fetch the instructor profile of the logged-in user
    instructor = get_object_or_404(Instructor, user=request.user)

    
    instructor.delete()
    messages.success(request, "Instructor profile deleted successfully!")
    return redirect('InstructorListView')  # Replace with your desired page

class InstructorListView(LoginRequiredMixin, ListView):
    model = Instructor
    template_name = 'lecture/instructor_details.html'
    context_object_name = 'instructor'
    paginate_by = 10

    def get_queryset(self):
        # Filter instructors based on the logged-in user
        return Instructor.objects.filter(user=self.request.user)

# Display all Levels
def level_list(request):
    levels = Level.objects.all()
    return render(request, 'lecture/level_list.html', {'levels': levels})

# Add new Level
def add_level(request):
    if request.method == "POST":
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('level_list')
    else:
        form = LevelForm()
    return render(request, 'lecture/add_level.html', {'form': form})


# Update Level
def update_level(request, pk):
    level = get_object_or_404(Level, pk=pk)
    if request.method == "POST":
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            return redirect('level_list')
    else:
        form = LevelForm(instance=level)
    return render(request, 'lecture/update_level.html', {'form': form})


def delete_level(request, pk):
    level = get_object_or_404(Level, pk=pk)
    level.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('level_list')
    
# END LEVEL

# START Language
# Display all language
def language_list(request):
    language = Language.objects.all()
    return render(request, 'lecture/language_list.html', {'language': language})


# Add new Level
def add_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = LanguageForm()
    return render(request, 'lecture/add_language.html', {'form': form})


def update_language(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = LanguageForm(instance=language)
    return render(request, 'lecture/update_language.html', {'form': form})


def delete_language(request, pk):
    level = get_object_or_404(Language, pk=pk)
    level.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('language_list')
# END LANGUAGE 

# START COURSE
@login_required
def course_list(request):
    # Filter courses where the author is the currently logged-in user
    courses = Course.objects.filter(author__user=request.user)
    return render(request, 'lecture/course_list.html', {'courses': courses})

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, user=request.user)  # Pass user to the form
        if form.is_valid():
            course = form.save(commit=False)
            instructor = Instructor.objects.filter(user=request.user).first()  # Fetch the current instructor
            if instructor:
                course.author = instructor
                course.save()
                messages.success(request, "Course added successfully!")
                return redirect('course_list')
            else:
                messages.error(request, "You are not an instructor. Please contact the admin.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseForm(user=request.user)  # Pass user to the form
    
    instructor = Instructor.objects.filter(user=request.user).first()
    return render(request, 'lecture/add_course.html', {'form': form, 'instructor': instructor})

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
        # print(course.author)
        # print(form)
    return render(request, 'lecture/update_course.html', {'form': form,'course':course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# END COURSE

# START Sub Category
# Display all categories
def category_display(request):
    categories = Categoriestheory.objects.all()
    return render(request, 'lecture/category_display.html', {'categories': categories})

# Create a new category
def category_create(request):
    if request.method == 'POST':
        form = CategoriestheoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_display')
    else:
        form = CategoriestheoryForm()
    return render(request, 'lecture/category_create.html', {'form': form})

# Update an existing category
def category_update(request, pk):
    category = get_object_or_404(Categoriestheory, pk=pk)
    if request.method == 'POST':
        form = CategoriestheoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_display')
    else:
        form = CategoriestheoryForm(instance=category)
    return render(request, 'lecture/category_update.html', {'form': form})

# Delete a category
def category_delete(request, pk):
    category = get_object_or_404(Categoriestheory, pk=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('category_list')

#END Sub Category

# START Course Resources
def add_course_resource(request):
    if request.method == 'POST':
        form = CourseResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource added successfully!")
            return redirect('resource_list')
    else:
        form = CourseResourceForm(user = request.user)
    return render(request, 'lecture/add_resource.html', {'form': form})


def resource_list(request):
    try:
        auther = Instructor.objects.get( user = request.user)
        my_courses = Course.objects.filter(author = auther)
        resource = CourseResource.objects.filter(course__in= my_courses)
        context = {'resources' : resource}
    except:
        context = {'resources' : None}
    return render(request, 'lecture/resource_list.html', context)

@login_required
def update_course_resource(request, resource_id):
    resource = get_object_or_404(CourseResource, id=resource_id)
    if request.method == 'POST':
        form = CourseResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully!")
            return redirect('resource_list')
    else:
        form = CourseResourceForm(instance=resource, user = request.user)
    return render(request, 'lecture/update_resource.html', {'form': form})

@login_required
def delete_course_resource(request, resource_id):
    resource = get_object_or_404(CourseResource, id=resource_id)
    resource.delete()
    messages.success(request, "Resource deleted successfully!")
    return redirect('resource_list')

# END Course Resources

def add_requirement(request):
    if request.method == 'POST':
        form = RequirementsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Requirement added successfully!")
            return redirect('requirement_list')
    else:
        form = RequirementsForm(user = request.user)
    return render(request, 'lecture/add_requirement.html', {'form': form})

def requirement_list(request):
    try:
        auther = Instructor.objects.get( user = request.user)
        my_courses = Course.objects.filter(author = auther)
        requirement = Requirements.objects.filter(course__in= my_courses)
        context = {'requirements' : requirement}
    except:
        context = {'requirements' : None}
    return render(request, 'lecture/requirement_list.html', context)

def update_requirement(request, requirement_id):
    requirement = get_object_or_404(Requirements, id=requirement_id)
    if request.method == 'POST':
        form = RequirementsForm(request.POST, instance=requirement)
        if form.is_valid():
            form.save()
            messages.success(request, "Requirement updated successfully!")
            return redirect('requirement_list')
    else:
        form = RequirementsForm(instance=requirement, user = request.user)
    return render(request, 'lecture/update_requirement.html', {'form': form})

def delete_requirement(request, requirement_id):
    requirement = get_object_or_404(Requirements, id=requirement_id)
    if request.method == 'POST':
        requirement.delete()
        messages.success(request, "Requirement deleted successfully!")
    return redirect('requirement_list')    



# Add a lesson
@login_required
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson added successfully!")
            return redirect('lesson_list')
    else:
        form = LessonForm(user = request.user)
    return render(request, 'lecture/add_lesson.html', {'form': form})

# Display all lessons
@login_required
def lesson_list(request):
    try:
        auther = Instructor.objects.get( user = request.user)
        my_course = Course.objects.filter(author = auther)
        lessons = Lesson.objects.filter(course__in= my_course)
        return render(request, 'lecture/lesson_list.html', {'lessons': lessons})
    except:
        return render(request, 'lecture/lesson_list.html')
    

# Update a lesson
def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=lesson, user = request.user)
    return render(request, 'lecture/update_lesson.html', {'form': form})

# Delete a lesson
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
    return redirect('lesson_list')


# Add a video or playlist url
# not needed, since yt video link not doing
def add_video(request):
    if request.method == 'POST':
        form = VideosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Video added successfully!")
            return redirect('video_list')
    else:
        form = VideosForm()
    return render(request, 'lecture/add_video.html', {'form': form})

# Display all videos or playlist url
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'lecture/video_list.html', {'videos': videos})

# Update a video or playlist url
def update_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully!")
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'lecture/update_video.html', {'form': form})

# Delete a video or playlist url
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully!")
    return redirect('video_list')


# Create a video
def create_video(request):
    if request.method == 'POST':
        form = VideosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Video added successfully!")
            return redirect('view_video')
    else:
        form = VideosForm(user = request.user)
    return render(request, 'lecture/create_video.html', {'form': form})

# list a video
def view_video(request):
    try:
        auther = Instructor.objects.get( user = request.user)
        my_course = Course.objects.filter(author = auther)
        videos = VideoModel.objects.filter(course__in = my_course)
        context = {'videos' : videos}
    except:
        context = {'videos' : None}
    return render(request, 'lecture/view_video.html', context)

# update a video
def video_update(request, video_id):
    video = get_object_or_404(VideoModel, id=video_id)
    if request.method == 'POST':
        form = VideosForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully!")
            return redirect('view_video')
    else:
        form = VideosForm(instance=video, user = request.user)
    return render(request, 'lecture/video_update.html', {'form': form})

# Delete a video
def delete_videos(request, video_id):
    video = get_object_or_404(VideoModel, id=video_id)
    if request.method == 'POST':
        VideoModel.delete()
        messages.success(request, "Video deleted successfully!")
    return redirect('video_list')


# test - quiz
def create_quiz(request):
    # course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()  # Save the quiz instance
            return redirect('add_questions', quiz_id=quiz.id)  # Redirect to the page to add questions
    else:
        quiz_form = QuizForm(user = request.user)
    return render(request, 'lecture/quiz/create_quiz.html', {'quiz_form': quiz_form})


def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, quiz=quiz)  # Pass quiz to the form
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz  # Explicitly set the quiz for the question
            question.save()
            return redirect('add_questions', quiz_id=quiz.id)  # Redirect to add another question or finish
    else:
        question_form = QuestionForm(initial={'quiz': quiz}, quiz=quiz)  # Pre-fill the quiz field and limit queryset    
    return render(request, 'lecture/quiz/add_questions.html', {'question_form': question_form, 'quiz': quiz})



def list_quiz(request):
    try:
        auther = Instructor.objects.get( user = request.user)
        my_courses = Course.objects.filter(author = auther)
        quizzes = Quiz.objects.filter(course__in= my_courses)
        
        
        context = {'quizzes' : quizzes}
    except:
        context = {'quizzes' : None}
    
    
    return render(request, 'lecture/quiz/list_quiz.html', context)

def delete_quiz(request,quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    quiz.delete()
    messages.success(request, "Quiz deleted successfully!")
    return redirect('list_quiz')

def edit_quiz(request,quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance = quiz )
        if quiz_form.is_valid():
            quiz_form.save()
            messages.success(request, "Quiz edited successfully!")
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm( instance = quiz, user = request.user )
    return render(request, 'lecture/quiz/edit_quiz.html', {'quiz_form':quiz_form} )



def get_quiz_results_for_course(request, quiz_id):
    # Step 1: Get the quiz for the given course (assuming there's one quiz per course)
    quiz = get_object_or_404(Quiz, id=quiz_id) 
    quiz_results = QuizResult.objects.filter(quiz=quiz).select_related('quiz')

    return render(request, 'lecture/quiz/quiz_results.html', {'quiz_results':quiz_results} )

def verify_result(request, quiz_result_id):
    quiz_result = get_object_or_404(QuizResult, id=quiz_result_id)
    certificate_obj, created =  Certificate.objects.get_or_create(
                quiz_result = quiz_result,
                verified = True,
            )
    print('reached')
    return redirect('quiz_results', quiz_id = quiz_result.quiz.id)