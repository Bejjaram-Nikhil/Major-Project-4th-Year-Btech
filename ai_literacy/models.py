from django.db import models
from accounts.models import User

class AILiteracyFramework(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    discipline = models.CharField(max_length=100, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frameworks')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class LearningModule(models.Model):
    framework = models.ForeignKey(AILiteracyFramework, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=30)
    video_url = models.URLField(blank=True)
    document = models.FileField(upload_to='learning_materials/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['framework', 'order']
    
    def __str__(self):
        return f"{self.framework.title} - {self.title}"

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['student', 'module']
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.module.title} ({self.progress_percentage}%)"
