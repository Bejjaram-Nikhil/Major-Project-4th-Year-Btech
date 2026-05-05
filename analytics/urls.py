from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_home, name='home'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('surveys/create/', views.survey_create, name='survey_create'),
    path('surveys/<int:pk>/', views.survey_detail, name='survey_detail'),
    path('surveys/<int:pk>/take/', views.take_survey, name='take_survey'),
    path('surveys/<int:pk>/responses/', views.survey_responses, name='survey_responses'),
    
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/generate-readiness/', views.generate_readiness_report, name='generate_readiness_report'),
    path('reports/generate-gender/', views.generate_gender_report, name='generate_gender_report'),
    path('reports/generate-discipline/', views.generate_discipline_report, name='generate_discipline_report'),
    
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
]
