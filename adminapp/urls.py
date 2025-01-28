from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('admin_approval_view', views.admin_approval_view, name='admin_approval'),
        path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
        
        path('instructor_list', views.instructor_list, name='instructor_list'),
        path('student_list', views.student_list, name='student_list'),
        path('verified_results', views.get_verified_quiz_results, name='verified_results'),
        path('upload_certificate/<int:verified_quiz_result_id>/',views.upload_certificate,name='upload_certificate')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

