from django.urls import path
from . import views

app_name = 'ai_literacy'

urlpatterns = [
    path('', views.framework_list, name='framework_list'),
    path('frameworks/', views.framework_list, name='framework_list'),
    path('frameworks/create/', views.framework_create, name='framework_create'),
    path('frameworks/<int:pk>/', views.framework_detail, name='framework_detail'),
    path('frameworks/<int:pk>/edit/', views.framework_edit, name='framework_edit'),
    path('frameworks/<int:pk>/delete/', views.framework_delete, name='framework_delete'),
    
    path('modules/', views.module_list, name='module_list'),
    path('modules/create/', views.module_create, name='module_create'),
    path('modules/<int:pk>/', views.module_detail, name='module_detail'),
    path('modules/<int:pk>/edit/', views.module_edit, name='module_edit'),
    path('modules/<int:pk>/delete/', views.module_delete, name='module_delete'),
    path('modules/<int:pk>/start/', views.module_start, name='module_start'),
    path('modules/<int:pk>/complete/', views.module_complete, name='module_complete'),
    
    path('my-progress/', views.my_progress, name='my_progress'),
]
