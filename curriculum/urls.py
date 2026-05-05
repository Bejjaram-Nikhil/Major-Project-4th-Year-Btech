from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    path('', views.curriculum_list, name='curriculum_list'),
    path('integrations/', views.curriculum_list, name='curriculum_list'),
    path('integrations/create/', views.curriculum_create, name='curriculum_create'),
    path('integrations/<int:pk>/', views.curriculum_detail, name='curriculum_detail'),
    path('integrations/<int:pk>/edit/', views.curriculum_edit, name='curriculum_edit'),
    
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:pk>/submit/', views.assignment_submit, name='assignment_submit'),
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'),
    path('submissions/<int:pk>/grade/', views.grade_submission, name='grade_submission'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
