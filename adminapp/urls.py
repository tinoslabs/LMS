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

        # quiz
        path('verified_results', views.get_verified_quiz_results, name='verified_results'),
        path('upload_certificate/<int:verified_quiz_result_id>/',views.upload_certificate,name='upload_certificate'),
        
        # all courses
        path('all_courses', views.all_courses, name='all_courses'),
        path('all_users_list', views.all_users_list, name='all_users_list'),

        # add or edit user
        path('add_edit_user',views.add_edit_user, name = 'add_edit_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

