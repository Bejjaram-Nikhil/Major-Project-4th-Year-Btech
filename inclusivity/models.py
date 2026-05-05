from django.db import models
from accounts.models import User

class InterventionProgram(models.Model):
    TARGET_GROUPS = [
        ('gender_gap', 'Gender Gap Reduction'),
        ('discipline_gap', 'Discipline Diversity'),
        ('cultural_gap', 'Cultural Inclusion'),
        ('skill_gap', 'Skill Development'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_group = models.CharField(max_length=50, choices=TARGET_GROUPS)
    objectives = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coordinated_programs')
    max_participants = models.IntegerField(default=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class MentorshipProgram(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discipline = models.CharField(max_length=100, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoring')
    max_mentees = models.IntegerField(default=5)
    current_mentees = models.IntegerField(default=0)
    is_accepting = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.mentor.get_full_name()}"

class MentorshipEnrollment(models.Model):
    program = models.ForeignKey(MentorshipProgram, on_delete=models.CASCADE, related_name='enrollments')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
    ], default='active')
    progress_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['program', 'mentee']

class SupportResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=50, choices=[
        ('tutorial', 'Tutorial'),
        ('guide', 'Guide'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('tool', 'Tool'),
    ])
    target_audience = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='support_resources/', blank=True, null=True)
    url = models.URLField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
