from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    # Questionnaire URLs
    path('questionnaires/', views.questionnaire_list, name='questionnaire_list'),
    path('questionnaires/<int:pk>/', views.questionnaire_detail, name='questionnaire_detail'),
    path('questionnaires/create/', views.questionnaire_create, name='questionnaire_create'),
    path('questionnaires/<int:pk>/edit/', views.questionnaire_edit, name='questionnaire_edit'),
    path('questionnaires/<int:pk>/delete/', views.questionnaire_delete, name='questionnaire_delete'),
    
    # Question URLs
    path('questionnaires/<int:questionnaire_id>/questions/create/', views.question_create, name='question_create'),  # NEW - This was missing
    path('questions/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),
    
    # Student Assessment URLs
    path('questionnaires/<int:pk>/take/', views.take_assessment, name='take_assessment'),
    path('attempts/<int:pk>/', views.attempt_detail, name='attempt_detail'),
    path('my-attempts/', views.my_attempts, name='my_attempts'),
]
