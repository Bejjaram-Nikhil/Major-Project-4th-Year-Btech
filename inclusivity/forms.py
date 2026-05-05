from django import forms
from .models import InterventionProgram, MentorshipProgram, MentorshipEnrollment, SupportResource

class InterventionForm(forms.ModelForm):
    class Meta:
        model = InterventionProgram
        fields = ['title', 'description', 'target_group', 'objectives', 'start_date', 'end_date', 'max_participants', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_group': forms.Select(attrs={'class': 'form-select'}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MentorshipForm(forms.ModelForm):
    class Meta:
        model = MentorshipProgram
        fields = ['title', 'description', 'discipline', 'max_mentees', 'is_accepting']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'discipline': forms.TextInput(attrs={'class': 'form-control'}),
            'max_mentees': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_accepting': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = MentorshipEnrollment
        fields = ['progress_notes']
        widgets = {
            'progress_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = SupportResource
        fields = ['title', 'description', 'resource_type', 'target_audience', 'file', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'target_audience': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
