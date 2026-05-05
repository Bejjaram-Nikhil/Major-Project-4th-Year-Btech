from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('researcher', 'Researcher'),
        ('admin', 'Administrator'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    discipline = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, default='India')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_year = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['-created_at']
