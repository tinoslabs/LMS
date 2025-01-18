from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('admin_approval_view', views.admin_approval_view, name='admin_approval'),
        path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
        
        path('instructor_list', views.instructor_list, name='instructor_list'),
        path('student_list', views.student_list, name='student_list'),
        
]