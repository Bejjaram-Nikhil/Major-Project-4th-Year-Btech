from django.db import models
from accounts.models import User

class CurriculumIntegration(models.Model):
    title = models.CharField(max_length=200)
    discipline = models.CharField(max_length=100)
    course_code = models.CharField(max_length=50)
    semester = models.IntegerField()
    description = models.TextField()
    learning_objectives = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.title}"

class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ('case_study', 'Case Study'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
        ('research', 'Research Paper'),
        ('practical', 'Practical Exercise'),
    ]
    
    curriculum = models.ForeignKey(CurriculumIntegration, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignment_type = models.CharField(max_length=50, choices=ASSIGNMENT_TYPES)
    instructions = models.TextField()
    due_date = models.DateTimeField()
    max_points = models.IntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/')
    submission_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='graded_submissions')
    graded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
