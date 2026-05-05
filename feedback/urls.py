from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    # User URLs
    path('submit/', views.feedback_create, name='feedback_create'),
    path('my-feedback/', views.my_feedback, name='my_feedback'),
    path('<int:pk>/', views.feedback_detail, name='feedback_detail'),
    
    # Admin URLs
    path('admin/list/', views.feedback_list_admin, name='feedback_list_admin'),
    path('admin/<int:pk>/', views.feedback_detail_admin, name='feedback_detail_admin'),
    path('admin/<int:pk>/respond/', views.feedback_respond, name='feedback_respond'),
    path('admin/<int:pk>/delete/', views.feedback_delete, name='feedback_delete'),  # NEW
]
