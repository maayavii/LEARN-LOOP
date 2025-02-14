from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('list/', views.list_exams, name='exam_list'),  # Lists all available exams
    path('exams/<int:exam_id>/', views.take_exam, name='take_exam'),  # Take an exam
    path('exams/<int:exam_id>/result/', views.view_result, name='view_result'),  # View exam result
    path('dashboard/', views.exam_dashboard, name='exam_dashboard'),  # Exam dashboard for analytics or overview
    path('create/', views.create_exam, name='create_exam'),  # Create a new exam
    path('user/<int:user_id>/exams/', views.user_exams, name='user-exams'),  # List exams created by a user
]
