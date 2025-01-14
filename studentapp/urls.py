from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        # path('student_profile', views.student_profile, name='student_profile'), defined in testapp
        path('list_my_course', views.list_my_course, name='list_my_course'),
        path('quiz_selection', views.quiz_selection, name='quiz_selection'),
        path('start_quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
        path('quiz/<int:quiz_id>/question/<int:question_index>/', views.quiz_question, name='quiz_question'),
        path('quiz/<int:quiz_id>/complete', views.quiz_complete, name='quiz_complete'),
        path('quiz-result/<int:quiz_result_id>/', views.quiz_result, name='quiz_result'),
        path('quiz_result_all', views.quiz_result_all, name='quiz_result_all'),
        
]

