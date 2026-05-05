from django.contrib import admin
from .models import AILiteracyFramework, LearningModule, StudentProgress

@admin.register(AILiteracyFramework)
class AILiteracyFrameworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'discipline', 'difficulty_level', 'created_by', 'is_active', 'created_at']
    list_filter = ['difficulty_level', 'discipline', 'is_active']
    search_fields = ['title', 'description']

@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'framework', 'order', 'duration_minutes', 'is_published', 'created_at']
    list_filter = ['framework', 'is_published']
    search_fields = ['title', 'description']

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'module', 'progress_percentage', 'started_at', 'completed_at']
    list_filter = ['started_at', 'completed_at']
    search_fields = ['student__username', 'module__title']
