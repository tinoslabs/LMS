# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.student_register, name='api-student-register'),
    path('auth/login/', views.student_login, name='api-student-login'),
    path('auth/logout/', views.logout_view, name='api-logout'),
    path('home/', views.home_page, name='api-home'),
]