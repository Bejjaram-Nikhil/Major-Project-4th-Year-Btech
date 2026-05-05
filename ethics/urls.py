from django.urls import path
from . import views

app_name = 'ethics'

urlpatterns = [
    path('', views.ethics_home, name='home'),
    path('case-studies/', views.case_study_list, name='case_study_list'),
    path('case-studies/create/', views.case_study_create, name='case_study_create'),
    path('case-studies/<int:pk>/', views.case_study_detail, name='case_study_detail'),
    path('case-studies/<int:pk>/edit/', views.case_study_edit, name='case_study_edit'), 
    
    path('forums/', views.forum_list, name='forum_list'),
    path('forums/create/', views.forum_create, name='forum_create'),
    path('forums/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('forums/<int:pk>/post/', views.create_post, name='create_post'),
    path('posts/<int:pk>/reply/', views.reply_post, name='reply_post'),
    
    path('principles/', views.principle_list, name='principle_list'),
    path('principles/create/', views.principle_create, name='principle_create'),
    path('principles/<int:pk>/', views.principle_detail, name='principle_detail'),
    path('principles/<int:pk>/edit/', views.principle_edit, name='principle_edit'),

]
