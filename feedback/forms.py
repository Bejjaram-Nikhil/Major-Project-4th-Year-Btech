from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'subject', 'message']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief summary of your feedback'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Provide detailed feedback...'
            }),
        }
        help_texts = {
            'subject': 'Keep it concise and descriptive',
            'message': 'Be as detailed as possible to help us understand your feedback better',
        }


class FeedbackResponseForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status', 'priority', 'admin_response']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your response to the user...'
            }),
        }
