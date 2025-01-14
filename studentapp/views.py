from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from testapp.models import User

from django.contrib import messages
from testapp.forms import UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect,render

from testapp.models import QuizResult,QuizAnswer,Question,Quiz,UserCourse,Categories,Course,Level,Video,Categoriestheory,Author,Language,CourseResource,What_u_learn,Requirements,Lesson,VideoModel,Instructor
from testapp.forms import CategoryForm,AuthorForm,LevelForm,LanguageForm,CourseForm,CategoriestheoryForm,CourseResourceForm,WhatULearnForm,RequirementsForm,LessonForm,VideoForm,VideosForm,PasswordChangeForm,InstructorForm
# from .settings import *

# @login_required
# def student_profile(request): defined in testapp
#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('student_profile')  
#     else:
#         profile_form = UserProfileForm(instance=request.user)
#     return render(request, 'users/student_profile.html', {'profile_form': profile_form})


def list_my_course(request):
    if not request.user.is_authenticated:
        return redirect('login_view')  

    # Query the user's courses
    courses = UserCourse.objects.filter(user=request.user).select_related('course', 'course__category', 'course__author')
    
    # Retrieve other data
    category = Categories.objects.all().order_by('id')[:6]
    theory = Categoriestheory.objects.all().order_by('id')[:6]
    courser = CourseResource.get_all_category(CourseResource)
    return render(request, 'student/list_my_course.html', {'courses':courses})



def quiz_selection(request):
    courses = UserCourse.objects.filter(user=request.user).select_related('course', 'course__category', 'course__author').prefetch_related('course__quizzes')

    return render(request, 'student/my_quiz_selection.html',{'courses':courses})

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # Get the user's already submitted answers for this quiz
    answered_questions = QuizAnswer.objects.filter(user=request.user, quiz=quiz)
    unanswered_questions = questions.exclude(id__in=answered_questions.values_list('question_id', flat=True))

    if unanswered_questions.exists():
        # If there are unanswered questions, get the first one
        next_question = unanswered_questions.first()
        questions_list = list(questions)
        question_index = questions_list.index(next_question) + 1  # Adjust for 1-based indexing

        # Redirect to the quiz_question view with the pending question
        return redirect('quiz_question', quiz_id=quiz.id, question_index=question_index)
    else:
        # If all questions are answered, redirect to quiz completion
        return redirect('quiz_complete', quiz_id=quiz.id)



@login_required
def quiz_question(request, quiz_id, question_index):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # Convert 1-based index to 0-based for internal processing
    zero_based_index = question_index - 1

    # Ensure the question_index is valid
    if zero_based_index >= 0 and zero_based_index < len(questions):
        question = questions[zero_based_index]

        # Get the user's already submitted answer for this question
        user_answer = QuizAnswer.objects.filter(user=request.user, quiz=quiz, question=question).first()
        selected_option = user_answer.selected_option if user_answer else None

        if request.method == 'POST':
            selected_option = request.POST.get('answer')

            # Save the user's answer for the current question
            if selected_option:
                quiz_answer, created = QuizAnswer.objects.get_or_create(
                    user=request.user,
                    quiz=quiz,
                    question=question,
                )
                quiz_answer.selected_option = int(selected_option)
                quiz_answer.save()

            # Redirect to the next unanswered question or finish the quiz
            # answered_questions = QuizAnswer.objects.filter(user=request.user, quiz=quiz)
            # unanswered_questions = questions.exclude(id__in=answered_questions.values_list('question_id', flat=True))

            # if unanswered_questions.exists():
            #     next_question = unanswered_questions.first()
            #     questions_list = list(questions)
            #     next_question_index = questions_list.index(next_question) + 1  # Adjust for 1-based indexing
            #     return redirect('quiz_question', quiz_id=quiz.id, question_index=next_question_index)
            # else:
            #     return redirect('quiz_complete', quiz_id=quiz.id)

            if zero_based_index >= 0 and zero_based_index < len(questions):
                next_question_index = zero_based_index + 2
                return redirect('quiz_question', quiz_id=quiz.id, question_index=next_question_index)
            else:
                return redirect('quiz_complete', quiz_id=quiz.id)

        return render(request, 'student/start_quiz.html', {
            'quiz': quiz,
            'question': question,
            'question_index': question_index,
            'selected_option': selected_option,  # Pass the selected option to the template
            'next_question_index': question_index + 1 if question_index < len(questions) else None,
            'previous_question_index': question_index - 1 if question_index > 1 else None,
            'total_questions': len(questions),
        })
    else:
        return redirect('quiz_complete', quiz_id=quiz.id)  # Redirect to quiz completion page if out of bounds

@login_required
def quiz_complete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_questions = quiz.questions.all()
    
    # Get the answers submitted by the user for this quiz
    quiz_answers = QuizAnswer.objects.filter(user=request.user, quiz=quiz)
    
    # Initialize counters for correct answers
    correct_answers = 0
    total_questions = quiz_questions.count()

    # Calculate the number of correct answers
    for quiz_answer in quiz_answers:
        correct_option = quiz_answer.question.correct_option  # Assuming `correct_option` field exists
        if quiz_answer.selected_option == correct_option:
            correct_answers += 1
    
    # Calculate score percentage
    if total_questions > 0:
        score_percentage = (correct_answers / total_questions) * 100
    else:
        score_percentage = 0
    
    # Save the result to the QuizResult model
    quiz_result, create = QuizResult.objects.get_or_create(
        user=request.user,
        quiz=quiz,
        # correct_answers=correct_answers,
        # total_questions=total_questions,
        # score_percentage=score_percentage
    )
    quiz_result.correct_answers=correct_answers
    quiz_result.total_questions=total_questions
    quiz_result.score_percentage=score_percentage
    quiz_result.save()

    # Redirect to the results display view
    return redirect('quiz_result', quiz_result_id=quiz_result.id)

@login_required
def quiz_result(request, quiz_result_id):
    quiz_result = get_object_or_404(QuizResult, id=quiz_result_id)
    
    quiz_answers = QuizAnswer.objects.filter(quiz=quiz_result.quiz, user=request.user)

    # Prepare data for the template
    result_data = []
    for answer in quiz_answers:
        result_data.append({
            'question': answer.question.question_text,
            'chosen_answer': getattr(answer.question, f"option_{answer.selected_option}", "N/A"),
            'is_correct': answer.selected_option == answer.question.correct_option,
        })

    return render(request, 'student/quiz_result.html', {
        'quiz_result': quiz_result,
        'quiz': quiz_result.quiz,
        'result_data': result_data,
    })


@login_required
def quiz_result_all(request):
    # Fetch all quiz results for the logged-in user
    quiz_results = QuizResult.objects.filter(user=request.user)

    return render(request, 'student/quiz_result_all.html', {
        'quiz_results': quiz_results,
    })