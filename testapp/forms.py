from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import Certificate,User,Categoriestheory,What_u_learn,Requirements,Lesson,Video,VideoModel,Instructor,CourseResource,Quiz



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        
          
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'profile_image']
        
        
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )
        
          
from .models import  Categories,Author,Level,Language,Course

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'
        
        
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['author_profile', 'name', 'about_author','designation']
        
# class InstructorForm(forms.ModelForm):
#     class Meta:
#         model = Instructor
#         fields = ['author_profile', 'name', 'about_author','designation']

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['about_author', 'designation']
        
        
class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = '__all__'
        
        
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'
        
               
# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = [
#             'featured_image', 'featured_video', 'title', 'author', 'category', 'level',
#             'description', 'price', 'discount', 'language', 'deadline', 'slug', 
#             'status', 'Certificate', 'is_free'
#         ]
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 5}),
#             'slug': forms.TextInput(attrs={'placeholder': 'Enter course slug'}),
#             'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
#         }

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = [
#             'featured_image', 'featured_video', 'title', 'category', 'level',
#             'description', 'price', 'discount', 'language', 'deadline', 'slug', 
#             'status', 'Certificate', 'is_free'
#         ]
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 5}),
#             'slug': forms.TextInput(attrs={'placeholder': 'Enter course slug'}),
#             'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  
#         super(CourseForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['author'].initial = user.instructor 
#             self.fields['author'].widget = forms.HiddenInput()  

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = [
#             'featured_image', 'featured_video', 'title', 'category', 'level',
#             'description', 'price', 'discount', 'language', 'deadline', 'slug', 
#             'status', 'Certificate', 'is_free', 'author'  # Include 'author'
#         ]
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 5}),
#             'slug': forms.TextInput(attrs={'placeholder': 'Enter course slug'}),
#             'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
#             'author': forms.HiddenInput(), 
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None) 
#         super(CourseForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['author'].initial = user.instructor 

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'featured_image', 'featured_video', 'title', 'category', 'level',
            'description', 'price', 'discount', 'language', 'deadline', 'slug',
            'status', 'Certificate', 'is_free'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'slug': forms.TextInput(attrs={'placeholder': 'Enter course slug'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CourseForm, self).__init__(*args, **kwargs)
        if user:
            pass
    
class CategoriestheoryForm(forms.ModelForm):
    class Meta:
        model = Categoriestheory
        fields = ['icon', 'name', 'title']   
        
        

class CourseResourceForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['course', 'resource_type', 'title', 'file']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter resource title'
                }),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"  
                    self.fields['title'].widget.attrs['placeholder'] = "Please add a course first"   
            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['title'].widget.attrs['placeholder'] = "Author details not provided" 
               
    

   
class WhatULearnForm(forms.ModelForm):
    class Meta:
        model = What_u_learn
        fields = ['course', 'points']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'points': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter points learned from the course'}),
        }

        
class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Requirements
        fields = ['course', 'points']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'points': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter requirement'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                # Filter courses by the logged-in instructor
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['points'].widget.attrs['placeholder'] = "Please add a course first"
                        
            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['points'].widget.attrs['placeholder'] =  'Author details not provided'
    
        
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'name']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lesson name'
            }),
        }
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                # Filter courses by the logged-in instructor
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['name'].widget.attrs['placeholder'] = "Please add a course first"

            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['name'].widget.attrs['placeholder'] =  'Author details not provided'
        


# for video or playlist link 
# # not needed, since yt video link not doing    
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['serial_number', 'thumbnail', 'course', 'lesson', 'title', 'youtube_id', 'time_duration', 'preview']
        widgets = {
            'serial_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter serial number'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter video title'}),
            'youtube_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter YouTube ID'}),
            'time_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in seconds'}),
            'preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# for video file upload   
class VideosForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['serial_number', 'thumbnail', 'course', 'lesson', 'title', 'video', 'time_duration', 'preview']
        widgets = {
            'serial_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter serial number'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter video title'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload video'}),
            'time_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in seconds'}),
            'preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                # Filter courses by the logged-in instructor
                courses = Course.objects.filter(author=instructor)
                if courses.exists():
                    self.fields['course'].queryset = courses
                    lessons = Lesson.objects.filter(course__in = courses)
                    if lessons.exists():
                        self.fields['lesson'].queryset = lessons
                    else:
                        self.fields['lesson'].empty_label = "Lessons not added"
                else:
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['lesson'].queryset = Lesson.objects.none()
                    self.fields['lesson'].empty_label = "Please add a course"
                    self.fields['title'].widget.attrs['placeholder'] = "Please add a course first"
                    

            except Instructor.DoesNotExist:
                # If the user is not an instructor, no courses are available
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['lesson'].queryset = Lesson.objects.none()
                self.fields['lesson'].empty_label = "Please add a course"
                self.fields['title'].widget.attrs['placeholder'] =  'Author details not provided'
        

# test - quiz
# Form for creating/editing a quiz


from django import forms
from .models import Quiz, Question, Course

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'title']

        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quiz Title'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user passed during form initialization
        super().__init__(*args, **kwargs)
        if user:
            try:
                instructor = Instructor.objects.get(user=user)
                courses = Course.objects.filter(author=instructor)
                
                # Filter out the selected course if in edit mode
                if self.instance and self.instance.pk:
                    # Ensure the current quiz's course is in the filtered queryset
                    self.fields['course'].queryset = courses.filter(id=self.instance.course.id)
                else:
                    self.fields['course'].queryset = courses  # Limit courses to those authored by the instructor
                
                if not courses.exists():
                    self.fields['course'].queryset = Course.objects.none()
                    self.fields['course'].empty_label = "No courses available"
                    self.fields['title'].widget.attrs['placeholder'] = "Please add a course first"
            except Instructor.DoesNotExist:
                self.fields['course'].queryset = Course.objects.none()
                self.fields['course'].empty_label = "No courses available"
                self.fields['title'].widget.attrs['placeholder'] = "Author details not provided"
               



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']

        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-select'}),
            'question_text': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Question'
            }),
            'option_1': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter First Option'
            }),
            'option_2': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Second Option'
            }),
            'option_3': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Third Option'
            }),
            'option_4': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Fourth Option'
            }),
            'correct_option': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz', None)  # Extract the specific quiz passed
        super().__init__(*args, **kwargs)
        if quiz:
            self.fields['quiz'].queryset = Quiz.objects.filter(id=quiz.id)  # Limit to the specific quiz
        else:
            self.fields['quiz'].queryset = Quiz.objects.none()  # Empty queryset if no quiz provided
            self.fields['quiz'].empty_label = "No Quiz available"


class CertificateUploadForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ["certificate_file"]

