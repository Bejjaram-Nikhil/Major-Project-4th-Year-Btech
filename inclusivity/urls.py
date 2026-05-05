from django.urls import path
from . import views

app_name = 'inclusivity'

urlpatterns = [
    path('', views.inclusivity_home, name='home'),
    path('interventions/', views.intervention_list, name='intervention_list'),
    path('interventions/create/', views.intervention_create, name='intervention_create'),
    path('interventions/<int:pk>/', views.intervention_detail, name='intervention_detail'),
    
    path('mentorship/', views.mentorship_list, name='mentorship_list'),
    path('mentorship/create/', views.mentorship_create, name='mentorship_create'),
    path('mentorship/<int:pk>/', views.mentorship_detail, name='mentorship_detail'),
    path('mentorship/<int:pk>/enroll/', views.mentorship_enroll, name='mentorship_enroll'),
    path('my-mentorships/', views.my_mentorships, name='my_mentorships'),
    
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/create/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
]
