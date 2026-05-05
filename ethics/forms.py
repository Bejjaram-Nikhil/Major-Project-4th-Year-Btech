from django import forms
from .models import EthicalCaseStudy, DiscussionForum, DiscussionPost, EthicalPrinciple

class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = EthicalCaseStudy
        fields = ['title', 'description', 'scenario', 'discipline', 'difficulty_level', 'learning_objectives', 'discussion_questions', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'scenario': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'discipline': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
            'learning_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'discussion_questions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ForumForm(forms.ModelForm):
    class Meta:
        model = DiscussionForum
        fields = ['case_study', 'title', 'description', 'is_active']
        widgets = {
            'case_study': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Share your thoughts...'}),
        }

class PrincipleForm(forms.ModelForm):
    class Meta:
        model = EthicalPrinciple
        fields = ['title', 'description', 'examples', 'category', 'resources']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'examples': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'resources': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
