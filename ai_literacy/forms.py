from django import forms
from .models import AILiteracyFramework, LearningModule

class AILiteracyFrameworkForm(forms.ModelForm):
    class Meta:
        model = AILiteracyFramework
        fields = ['title', 'description', 'discipline', 'difficulty_level', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'discipline': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class LearningModuleForm(forms.ModelForm):
    class Meta:
        model = LearningModule
        fields = ['framework', 'title', 'description', 'content', 'order', 'duration_minutes', 'video_url', 'document', 'is_published']
        widgets = {
            'framework': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
