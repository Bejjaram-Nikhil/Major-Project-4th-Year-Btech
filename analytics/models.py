from django.db import models
from accounts.models import User
import json

class SurveyTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    survey_type = models.CharField(max_length=50, choices=[
        ('readiness', 'AI Readiness'),
        ('satisfaction', 'Satisfaction'),
        ('relevance', 'Relevance Perception'),
        ('feedback', 'General Feedback'),
    ])
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class SurveyResponse(models.Model):
    survey = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE, related_name='responses')
    respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_responses')
    response_data = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['survey', 'respondent']

class AnalyticalReport(models.Model):
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=[
        ('readiness', 'Readiness Analysis'),
        ('gender', 'Gender Gap Analysis'),
        ('discipline', 'Discipline Analysis'),
        ('satisfaction', 'Satisfaction Report'),
        ('comprehensive', 'Comprehensive Report'),
    ])
    description = models.TextField()
    methodology = models.TextField()
    findings = models.TextField()
    recommendations = models.TextField()
    statistical_data = models.JSONField(default=dict)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.generated_at.strftime('%Y-%m-%d')}"

class StatisticalTest(models.Model):
    report = models.ForeignKey(AnalyticalReport, on_delete=models.CASCADE, related_name='statistical_tests')
    test_name = models.CharField(max_length=100)
    test_type = models.CharField(max_length=50, choices=[
        ('kruskal_wallis', 'Kruskal-Wallis H-test'),
        ('mann_whitney', 'Mann-Whitney U-test'),
        ('chi_square', 'Chi-Square Test'),
        ('anova', 'ANOVA'),
    ])
    variables_tested = models.CharField(max_length=200)
    test_statistic = models.FloatField()
    p_value = models.FloatField()
    significance_level = models.FloatField(default=0.05)
    is_significant = models.BooleanField()
    interpretation = models.TextField()
    
    def __str__(self):
        return f"{self.test_name} - p={self.p_value}"
