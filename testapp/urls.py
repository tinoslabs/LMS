# urls.py
from django.urls import path
# from .views import register_view
from .import views
# from .views import admin_approval_view
from .views import AuthorCreateView, AuthorListView, AuthorUpdateView, AuthorDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login_view/', views.login_view, name='login_view'),
    # path('logout', views.logout, name='logout'),
    path('logout', views.logout_view, name='logout'),
    path('register_view/', views.register_view, name='register'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    # path('profile_view',views.profile_view,name='profile_view'),
    path('profile_view', views.profile_view, name='profile_view'),
    path('student_profile', views.profile_view, name='student_profile'),
    path('lecture_profile', views.profile_view, name='lecture_profile'),
    path('change_password/', views.change_password, name='change_password'),
    # path('lecture_password', views.lecture_password, name='lecture_password'),
    # path('student_password', views.student_password, name='student_password'),
      
       
    path('student_dashboard',views.student_dashboard,name='student_dashboard'),
    # path('instructor_dashboard', views.instructor_dashboard,name='instructor_dashboard'),
    # path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'), moved
    # path('index',views.index, name='index'),
    
    # path('admin_approval_view', admin_approval_view, name='admin_approval'),
    
    # path('profile', profile_view, name='profile'),
       
    path('base', views.BASE, name='base'),
    path('404', views.PAGE_NOT_FOUND, name='404'),
        
    # path('accounts/register/', user_login.REGISTER, name='register'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('doLogin',user_login.Do_LOGIN,name='doLogin'),
    # path('logout/', user_login.LOGOUT, name='logout'),
    # path('accounts/profile', user_login.PROFILE,name='profile'),
    
    # path('register_view', user_login.register_view, name='register_view'),
    # path('login_view', user_login.login_view, name='login_view'),
        
    # path('home', views.HOME, name='home'),
    path('', views.index, name='index'),  
    path('courses', views.SINGLE_COURSE, name='single_cousre'),
    path('courses/filter_course',views.filter_course,name="filter_course"),
    # path('courses/<int:course_id>',views.COURSE_DETAILS,name="course_details"),

    path('about',views.ABOUT_US,name='about_us'),
    path('search', views.SEARCH_COURSE, name='search_cousre'),
           
    path('checkout/<int:course_id>',views.CHECKOUT,name='checkout'),
    path('my-course',views.MY_COURSE,name='my_course'),
    path('course/<int:course_id>/watch-course/<int:video_id>',views.WATCH_COURSE,name='watch_course'), 
    
    path('contact_us', views.contact_us, name='contact_us'),
    path('about_us', views.about_us, name='about_us'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course_watch', views.course_watch, name='course_watch'),
        
    # path('teachers',views.teachers, name='teachers'),
    # path('teachers_details', views.teachers_details, name='teachers_details'),
    # path('lecture_dashboard', views.lecture_dashboard, name='lecture_dashboard'),
    # path('account',views.account, name='account'),
    path('form',views.form,name='form'),   # template not available
        
    # path('category_list/', views.category_list, name='category_list'), moved
    # path('add_category/', views.add_category, name='add_category'), moved
    # path('update_category/<int:category_id>/', views.update_category, name='update_category'), moved
    # path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'), moved
            
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('add_author', AuthorCreateView.as_view(), name='add_author'),
    path('AuthorUpdateView/<int:pk>/', AuthorUpdateView.as_view(), name='update_author'),
    path('AuthorDeleteView/<int:pk>/', AuthorDeleteView.as_view(), name='delete_author'),
    # path('check_out', views.check_out, name='check_out'),
           
    # path('level_list', views.level_list, name='level_list'), moved
    # path('add_level', views.add_level, name='add_level'), moved
    # path('update_level/<int:pk>/', views.update_level, name='update_level'), moved
    # path('delete_level/<int:pk>/', views.delete_level, name='delete_level'), moved
        
    # path('add_language/', views.add_language, name='add_language'), moved
    # path('language_list', views.language_list, name='language_list'), moved
    # path('update_language/<int:pk>/', views.update_language, name='update_language'), moved
    # path('delete_language/<int:pk>/', views.delete_language, name='delete_language'), moved
        
    # path('course_list/', views.course_list, name='course_list'), moved
    # path('courses/<int:course_id>/', views.course_detail, name='course_detail'), moved
    # path('add_course', views.add_course, name='add_course'), moved
    # path('courses/<int:course_id>/edit/', views.update_course, name='update_course'), moved
    # path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'), moved
        
    # # sub category in front-end 
    # path('category_display', views.category_display, name='category_display'), moved
    # path('category_create', views.category_create, name='category_create'), moved
    # path('categories/<int:pk>/edit/', views.category_update, name='category_update'),  moved
    # path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'), moved
        
    # path('resources/add/', views.add_course_resource, name='add_resource'), moved
    # path('resources/', views.resource_list, name='resource_list'), moved
    # path('update_course_resource/<int:resource_id>/', views.update_course_resource, name='update_course_resource'), moved
    # path('resources/delete/<int:resource_id>/', views.delete_course_resource, name='delete_resource'), moved
        
    path('add_what_u_learn/', views.add_what_u_learn, name='add_what_u_learn'),
    path('what_u_learn_list/', views.what_u_learn_list, name='what_u_learn_list'),
    path('update_what_u_learn/edit/<int:entry_id>/', views.update_what_u_learn, name='update_what_u_learn'),
    path('delete_what_u_learn/<int:entry_id>/', views.delete_what_u_learn, name='delete_what_u_learn'),
        
    # path('add_requirement/', views.add_requirement, name='add_requirement'), moved
    # path('requirement_list/', views.requirement_list, name='requirement_list'), moved
    # path('update_requirement/<int:requirement_id>/', views.update_requirement, name='update_requirement'), moved
    # path('delete_requirement/<int:requirement_id>/', views.delete_requirement, name='delete_requirement'), moved
        
    # path('add_lesson/', views.add_lesson, name='add_lesson'), moved
    # path('lessons/', views.lesson_list, name='lesson_list'), moved
    # path('update_lesson/<int:lesson_id>/', views.update_lesson, name='update_lesson'), moved
    # path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'), moved
        
    # path('add_video/', views.add_video, name='add_video'), moved
    # path('video_list/', views.video_list, name='video_list'), moved
    # path('update_video/<int:video_id>/', views.update_video, name='update_video'), moved
    # path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'), moved
     
     
    path('user', views.user, name='user'),    
    path('create_user',views.create_user, name='create_user'),
    path('all_courses', views.all_courses, name='all_courses'),
      
    # path('lecture_profile',views.lecture_profile,name='lecture_profile'),
        
    # path('create_video',views.create_video, name='create_video'), moved
    # path('view_video',views.view_video, name='view_video'), moved
    # path('video_update/<int:video_id>/',views.video_update, name='video_update'), moved
    # path('delete_videos/<int:video_id>/', views.delete_videos, name='delete_videos'), moved
    path('chat', views.chat, name='chat'),
    
    # path('list_my_course', views.list_my_course, name='list_my_course'), moved to studentapp
    # path('course_filter', views.course_filter, name='course_filter'),
    path('course_filter/', views.course_filter, name='course_filter'),   # to display all courses if the category_id is absent
    path('course_filter/<int:category_id>/', views.course_filter, name='course_filter'),
    
    # path('create_instructor',views.create_instructor, name='create_instructor'), moved
    # path('Instructor_ListView',InstructorListView.as_view(), name='InstructorListView'), moved
    # path('instructor/update/', views.update_instructor, name='update_instructor'), moved
    # path('instructor/delete/', views.delete_instructor, name='delete_instructor'), moved
    
    # for otp
    path('forgot-password/', views.request_otp_view, name='request_otp_view'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp_view'),

    # teachers list
    path('teachers',views.teachers, name='teachers'),  # all teachers list
    path('teachers_details/<int:teacher_id>/', views.teachers_details, name='teachers_details'), # single teachers detail   ... in html teachers-singel.html is placed need to replace.


]
