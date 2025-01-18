# views.py
from django.contrib.auth import authenticate, login,logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from lecturerapp.decorators import otp_required

# for otp
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.utils import timezone

# from django.contrib.auth.models import User
from .models import OTPModel
import secrets

from django.contrib import messages
from .models import User
from django.db.models import Count

# from .forms import UserRegistrationForm

from .models import VideoProgress,Categories,Course,Level,Video,Categoriestheory,Author,CourseResource,Language,What_u_learn,Requirements,Lesson,VideoModel,Instructor
from .forms import CategoryForm,UserRegistrationForm,AuthorForm,LevelForm,LanguageForm,CourseForm,CourseResourceForm,CategoriestheoryForm,WhatULearnForm,RequirementsForm,LessonForm,VideoForm,VideosForm,PasswordChangeForm,InstructorForm

from django.shortcuts import get_object_or_404, redirect,render

from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
# import razorpay
from time import time

from .models import UserCourse,Payment

# to register
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Set to False by default
            user.save()
            messages.success(request, 'Registration successful. Please wait for approval.')
            return redirect('login_view')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register-1.html', {'form': form})


# to login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use get() method
        password = request.POST.get('password')  # Use get() method

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('login_view')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'instructor' and not user.is_approved:
                messages.error(request, 'Your account is not approved yet.')
                return redirect('login_view')
            login(request, user)

            if user.is_superuser:
                return redirect('index')  
            elif user.role == 'instructor':
                return redirect('index') 
            elif user.role == 'student':
                return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password.')
    category=Categories.objects.all().order_by('id')[0:6]

    return render(request, 'registration/login-1.html',{'category':category})

from .forms import UserProfileForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            
            
            if request.user.role == 'admin':
                return redirect('admin_profile')  # Replace with the correct URL name for admin
            elif request.user.role == 'student':
                # print("Profile updated successfully")
                return redirect('student_profile')  # Replace with the correct URL name for student
            elif request.user.role == 'instructor':
                return redirect('lecture_profile')  # Replace with the correct URL name for instructor
        else:
            print("Form is not valid:", profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=request.user)

    # Render a template based on the role
    if request.user.role == 'admin':
        template_name = 'admin/admin_profile.html'
    elif request.user.role == 'student':
        template_name = 'users/student_profile.html'
    elif request.user.role == 'instructor':
        template_name = 'users/lecture_profile.html'
    else:
        template_name = 'admin/admin_profile.html'  # Fallback template for undefined roles

    context = {
        'profile_form': profile_form,
    }
    return render(request, template_name, context)


from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    # Role-based template rendering
    if request.user.role == 'admin':
        template_name = 'users/change_password_admin.html'
    elif request.user.role == 'instructor':
        template_name = 'users/change_password_instructor.html'
    elif request.user.role == 'student':
        template_name = 'users/change_password_student.html'
    else:
        template_name = 'users/change_password_default.html'  # Optional for unknown roles

    return render(request, template_name, {'form': form})


# @login_required
# def lecture_profile(request):  moved to lecturer app
#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('lecture_profile')  
#     else:
#         profile_form = UserProfileForm(instance=request.user)
#     return render(request, 'users/lecture_profile.html', {'profile_form': profile_form})

# @login_required
# def student_profile(request):  moved to student app
#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('student_profile')  
#     else:
#         profile_form = UserProfileForm(instance=request.user)
#     return render(request, 'users/student_profile.html', {'profile_form': profile_form})


def logout_view(request):
    auth_logout(request)  # Use Django's built-in logout function
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login_view')


# def instructor_dashboard(request):
#     return render(request,'instructor_dashboard.html')




def student_dashboard(request):
    return render(request,'student/student_dashboard.html')


def BASE(request):
    return render(request,'base.html')


def HOME(request):
    category=Categories.objects.all().order_by('id')[0:6]
    theory=Categoriestheory.objects.all().order_by('id')[0:6]
    course=Course.objects.filter(status='PUBLISH').order_by('-id')
    courser=CourseResource.get_all_category(CourseResource)
    # print(course)
    context={
        'category':category,
        'course':course,
        'theory':theory,
        'courser':courser, # type: ignore
    }
    return render(request,'Main/home.html',context)

def get_top_instructors():
    top_instructors = (
        User.objects.filter(role='instructor')
        .annotate(course_count=Count('instructor__course'))
        .order_by('-course_count')[:4]
    )
    return top_instructors

def index(request):
    category=Categories.objects.all().order_by('id')[0:6]
    theory=Categoriestheory.objects.all().order_by('id')[0:6]
    course=Course.objects.filter(status='PUBLISH').order_by('-id')
    courser=CourseResource.get_all_category(CourseResource)
    
    top_teachers = get_top_instructors

    context={
        'category':category,
        'course':course,
        'theory':theory,
        'courser':courser, 
        'top_teachers':top_teachers,
    }
    return render(request,'index.html',context)


def course_filter(request, category_id=None):
    # Get all categories for the sidebar or menu
    category = Categories.objects.all().order_by('id')[0:6]

    # If a category ID is provided, filter courses by category
    if category_id:
        selected_category = get_object_or_404(Categories, id=category_id)
        courses = Course.objects.filter(category=selected_category, status="PUBLISH")
    else:
        # If no category is selected, display all published courses
        courses = Course.objects.filter(status="PUBLISH")
        selected_category = None

    context = {
        'category': category,
        'courses': courses,
        'selected_category': selected_category,
    }
    return render(request, 'course_filter.html', context)


def SINGLE_COURSE(request):
    category=Categories.get_all_category(Categories) # type: ignore
    # theory=Theory.get_all_category(Theory)
    level=Level.objects.all()
    course = Course.objects.all()
    FeeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        # 'theory':theory,
        'level':level,
        'course':course,
        'FeeCourse_count':FeeCourse_count,
        'PaidCourse_count':PaidCourse_count,
    }
    return render(request,'Main/single_course.html',context)


def filter_course(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
      # print(category)
    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course= Course.objects.filter(category__id__in = category).order_by('-id')
    elif level:
          course = Course.objects.filter(level__id__in = level).order_by('-id')    
    else:
        course= Course.objects.all().order_by('-id')
    
    context ={
        'course':course
    }
    t = render_to_string('ajax/course.html',context)
    return JsonResponse({'data': t})




def ABOUT_US(request):
    category=Categories.get_all_category(Categories)
    context={
        'category':category,

    }
    return render(request,'Main/about_us.html',context)


def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    # tcourse = TheoryCourse.objects.filter(title__icontains = query)
    category=Categories.get_all_category(Categories)
   
    context = {
        'course':course,
        'category':category,
        # 'tcourse ':tcourse ,
    }
    return render(request,'search/search.html',context)


# not unsing anywhare
# def COURSE_DETAILS(request, course_id):
  
#     category=Categories.get_all_category(Categories)
#     time_duration = VideoModel.objects.filter(course__id=course_id).aggregate(sum=Sum('time_duration'))

#     course = Course.objects.filter(pk=course_id)

#     check_enroll = None
#     user  = request.user
#     if user.is_authenticated:
#         try:
#             check_enroll = UserCourse.objects.get(
#                 user=request.user,course=course_id
#             )
#         except UserCourse.DoesNotExist:
#             pass   

#     if course.exists():
#         course=course.first();
#     else:
#         return redirect('404')
    
#     context={
#         'course':course,
#         'category':category,
#         'time_duration':time_duration,
#         'check_enroll':check_enroll,
#     }
#     return render(request,'course/course_details.html',context)


# commen fun, used in lecture and admin
from django.db.models import Q

from django.db.models import Sum

def get_course_data(course_id, user=None):
    """
    Retrieves course details, lessons, and video progress. used in course_detail and WATCH_COURSE
    """
    course = get_object_or_404(Course, pk=course_id)
    course_time_duration = VideoModel.objects.filter(course=course).aggregate(sum=Sum('time_duration'))
    lessons = course.lesson_set.annotate(total_duration=Sum('videomodel__time_duration'))

    category = Categories.objects.all().order_by('id')[0:6] #category on nav bar 

    check_enroll = None
    

    if user and user.is_authenticated:
        check_enroll = UserCourse.objects.filter(user=user, course=course).first()
        
    return {
        'course': course,
        'course_time_duration': course_time_duration,
        'lessons': lessons,
        'check_enroll': check_enroll,
        'category':category
    }


def course_detail(request, course_id):
    course_data = get_course_data(course_id, request.user)   # another function, place just above
    return render(request, 'courses-detail.html', course_data)

def WATCH_COURSE(request, course_id, video_id):
    # category=Categories.objects.all().order_by('id')[0:6]
    course_data = get_course_data(course_id, request.user)
    Video = get_object_or_404(VideoModel, id=video_id, course=course_data['course'])
    course_data['Video'] = Video
    # course_data['category']=category
    return render(request, 'course/watch-course-updated.html', course_data)


def PAGE_NOT_FOUND(request):
    category=Categories.get_all_category(Categories)
    context={
      
        'category':category,
    }
    return render(request,'error/404.html',context)

 

# import razorpay

# Initialize the Razorpay client
# client = razorpay.Client(auth=("YOUR_API_KEY", "YOUR_API_SECRET"))

def CHECKOUT(request, course_id):
    # Get the course
    course = Course.objects.get(pk=course_id)
    action = request.GET.get('action')
    order = None

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to the registration page
        return redirect('accounts/register')  # Replace 'registration_url' with your actual registration URL name

    # If the course is free
    if course.price == 0:
        usercourse = UserCourse(
            user=request.user,
            course=course
        )
        usercourse.save()
        messages.success(request, 'Course has successfully enrolled!')
        return redirect('my_course')

    # If action is to create payment
    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address = request.POST.get('address')
            
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')

            amount = (course.price) * 100
            currency = "INR"
            notes = {
                "name": f'{first_name} {last_name}',
                "country": country,
                "address": address,
                "city": city,
                "state": state,
                "postcode": postcode,
                "phone": phone,
                "email": email,
                "order_comments": order_comments,
            }
            receipt = f"Edu-{int(time())}"
            order = client.order.create({
                'receipt': receipt,
                'amount': amount,
                'currency': currency,
                'notes': notes,
            })

            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    context = {
        'course': course,
        'order': order,
    }
    
    return render(request, 'checkout/checkout.html', context)

def MY_COURSE(request):
    if not request.user.is_authenticated:
        return redirect('login_view')  

    course = UserCourse.objects.filter(user=request.user)
    category = Categories.objects.all().order_by('id')[:6]
    theory = Categoriestheory.objects.all().order_by('id')[:6]
    courser = CourseResource.get_all_category(CourseResource)

    context = {
        'course': course,
        'category': category,
        'theory': theory,
        'courser': courser,
    }
    return render(request, 'course/my-course.html', context)

    # print(course)

# def WATCH_COURSE(request, course_id, video_id):
    
#     course = get_object_or_404(Course, id=course_id)
#     lecture_number = request.GET.get("lecture", 1)
#     video = VideoModel.objects.get(course=course.id, serial_number=lecture_number)    
    
#     if video is None:
#         return redirect('404')
    
#     context={
#         'course':course,
#         'video':video,
        
#     }        
#     return render(request, 'course/watch-course-updated.html',context)


def contact_us(request):
    category=Categories.objects.all().order_by('id')[0:6]
    return render(request,'contact-us.html',{'category':category})

def about_us(request):
    category=Categories.objects.all().order_by('id')[0:6]
    return render(request,'about_us.html',{'category':category})

def course_watch(request):
    category=Categories.objects.all().order_by('id')[0:6]
    return render(request,'course-watch.html',{'category':category})

# def teachers(request):
#     return render(request,'teachers.html')

# def teachers_details(request):
#     return render(request,'teachers-details.html')

# def lecture_dashboard(request):
#     return render(request,'lecture/lecture_dashboard.html')

# def account(request):
#     return render(request,'lecture/account.html')

def form(request): # template not available
    return render(request,'lecture/form-basic.html')




# 1. Add (Create) Author
class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'lecture/author_form.html'
    success_url = reverse_lazy('author_list')

    def form_valid(self, form):
        messages.success(self.request, "Author added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add author. Please check the form fields.")
        return super().form_invalid(form)
    
    


# 2. Display (List) Authors
class AuthorListView(ListView):
    model = Author
    template_name = 'lecture/author_list.html'
    context_object_name = 'authors'
    paginate_by = 10  # Adjust as needed for pagination

# 3. Update Author
class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'lecture/author_update_form.html'
    success_url = reverse_lazy('author_list')

    def form_valid(self, form):
        messages.success(self.request, "Author updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update author. Please check the form fields.")
        return super().form_invalid(form)


# 4. Delete Author
class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('author_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Author deleted successfully!")
        return self.delete(request, *args, **kwargs)



def add_what_u_learn(request):
    if request.method == 'POST':
        form = WhatULearnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Points learned added successfully!")
            return redirect('what_u_learn_list')
    else:
        form = WhatULearnForm()
    return render(request, 'lecture/add_what_u_learn.html', {'form': form})


def what_u_learn_list(request):
    what_u_learn_entries = What_u_learn.objects.all()
    return render(request, 'lecture/what_u_learn_list.html', {'what_u_learn_entries': what_u_learn_entries})


def update_what_u_learn(request, entry_id):
    entry = get_object_or_404(What_u_learn, id=entry_id)
    if request.method == 'POST':
        form = WhatULearnForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Points learned updated successfully!")
            return redirect('what_u_learn_list')
    else:
        form = WhatULearnForm(instance=entry)
    return render(request, 'lecture/update_what_u_learn.html', {'form': form})


def delete_what_u_learn(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(What_u_learn, id=entry_id)
        entry.delete()
        messages.success(request, "Points learned deleted successfully!")
    return redirect('what_u_learn_list')
    
    
def user(request):
    students = User.objects.filter(role='student')
    instructors = User.objects.filter(role='instructor')
    admins = User.objects.filter(role='admin')
    return render(request, 'admin/users.html', {
        'students': students,
        'instructors': instructors,
        'admins': admins
    })
    
    
def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Set to False by default
            user.save()
            messages.success(request, 'Registration successful. Please wait for approval.')
            return redirect('login_view')
    else:
        form = UserRegistrationForm()

    return render(request, 'admin/user_register.html', {'form': form})


def all_courses(request):
    courses = Course.objects.all()
    return render(request,'admin/all_courses.html',{'courses':courses})

    
def chat(request):
    return render(request,'chatbot.html')


# def list_my_course(request): moved to studentapp
#     if not request.user.is_authenticated:
#         return redirect('login_view')  

#     # Query the user's courses
#     courses = UserCourse.objects.filter(user=request.user).select_related('course', 'course__category', 'course__author')
    
#     # Retrieve other data
#     category = Categories.objects.all().order_by('id')[:6]
#     theory = Categoriestheory.objects.all().order_by('id')[:6]
#     courser = CourseResource.get_all_category(CourseResource)

#     # Debugging output
#     # print(course)

#     # context = {
#     #     'course': course,
#     #     'category': category,
#     #     'theory': theory,
#     #     'courser': courser,
#     # }
#     return render(request, 'student/list_my_course.html', {'courses':courses})


# otp for password
# OTP Request View
def request_otp_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return render(request, 'registration/forgot_password.html', {'email': email})
        
        # Delete all previous OTPs for this user
        OTPModel.objects.filter(user=user).delete()

        # Generate OTP
        otp = str(secrets.randbelow(10**6)).zfill(6)
        otp_entry=OTPModel.objects.create(user=user, otp=otp)
        request.session['user_id'] = user.id
        request.session['otp_expiry'] = otp_entry.expiry.isoformat()

        # Send OTP via email
        send_mail(
            subject="Your Password Reset OTP",
            message=(
                f"Hi {user.username},\n\n"
                f"Your OTP is {otp}. It is valid until {otp_entry.expiry}.\n\n"
                "If you did not request a password reset, please ignore this email."
            ),
            from_email="amalsanthosh527@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )
        messages.success(request, "OTP sent successfully.")
        return redirect('verify_otp_view')

    return render(request, 'registration/forgot_password.html',{'step': 'request'})

# OTP Verification View
@otp_required
def verify_otp_view(request):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Session expired. Please request an OTP again.')
        return redirect('request_otp_view')

    if request.method == "POST":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        # Check OTP validity
        try:
            otp_entry = OTPModel.objects.get(otp=otp, user=user)
        except OTPModel.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try againn.')
            return render(request, 'registration/forgot_password.html', {
                'otp': otp,
                'new_password': new_password,
                'confirm_new_password': confirm_new_password,
                'step': 'verify',
            })

        # Check if OTP is expired
        if otp_entry.expiry < timezone.now():
            otp_entry.delete()
            messages.error(request, 'OTP expired. Please request a new OTP.')
            return redirect('request_otp_view')

        # Check password match
        if new_password != confirm_new_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/forgot_password.html', {
                'otp': otp,
                'new_password': new_password,
                'confirm_new_password': confirm_new_password,
                'step': 'verify',
            })

        # Reset the password
        user.set_password(new_password)
        user.save()
        otp_entry.delete()
        request.session.pop('user_id', None)
        request.session.pop('otp_expiry', None)
        messages.success(request, "Password reset successful. You can now log in.")
        return redirect('login_view')

    return render(request, 'registration/forgot_password.html', {'step': 'verify'})

# teachers in index page
def teachers(request):
    category=Categories.get_all_category(Categories).order_by('id')[0:6]


    teachers = User.objects.filter(role='instructor')

    context={
        'category':category,
        'teachers':teachers
        }
    return render(request,'teachers.html',context)


def teachers_details(request, teacher_id):
    category=Categories.get_all_category(Categories).order_by('id')[0:6]


    teacher = get_object_or_404(User,id = teacher_id)
    try:
        instructor = Instructor.objects.get(user = teacher)
        my_courses = Course.objects.filter(author = instructor)
        context={
            'category':category,
            'teacher':teacher,
            'instructor':instructor,
            'my_courses':my_courses
            }
    except:

        context={
            'category':category,
            'teacher':teacher,
            'instructor':None,
            'courses':None
            }
    
    return render(request,'teachers-details.html',context)

