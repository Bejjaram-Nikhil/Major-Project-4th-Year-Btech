from django.db import models
from accounts.models import User

class EthicalCaseStudy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    scenario = models.TextField()
    discipline = models.CharField(max_length=100, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    learning_objectives = models.TextField()
    discussion_questions = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class DiscussionForum(models.Model):
    case_study = models.ForeignKey(EthicalCaseStudy, on_delete=models.CASCADE, related_name='forums', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_forums')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class DiscussionPost(models.Model):
    forum = models.ForeignKey(DiscussionForum, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_posts')
    content = models.TextField()
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class EthicalPrinciple(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    examples = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('fairness', 'Fairness & Bias'),
        ('transparency', 'Transparency'),
        ('privacy', 'Privacy'),
        ('accountability', 'Accountability'),
        ('safety', 'Safety'),
    ])
    resources = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
