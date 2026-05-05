from django.db import models
from accounts.models import User

class ReadinessQuestionnaire(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical Knowledge'),
        ('conceptual', 'Conceptual Understanding'),
        ('application', 'Practical Application'),
        ('ethical', 'Ethical Awareness'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    discipline_specific = models.CharField(max_length=100, blank=True)
    total_questions = models.IntegerField(default=0)
    time_limit_minutes = models.IntegerField(default=30)
    passing_score = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('rating', 'Rating Scale'),
        ('text', 'Text Response'),
    ]
    
    questionnaire = models.ForeignKey(ReadinessQuestionnaire, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.IntegerField(default=0)
    points = models.IntegerField(default=1)
    explanation = models.TextField(blank=True)
    
    class Meta:
        ordering = ['questionnaire', 'order']
    
    def __str__(self):
        return f"{self.questionnaire.title} - Q{self.order}"

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['question', 'order']

class AssessmentAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_attempts')
    questionnaire = models.ForeignKey(ReadinessQuestionnaire, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_points = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.questionnaire.title} ({self.score}%)"

class StudentResponse(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, null=True, blank=True)
    text_response = models.TextField(blank=True)
    rating_value = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['attempt', 'question']
