from django import forms
from .models import CurriculumIntegration, Assignment, AssignmentSubmission

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = CurriculumIntegration
        fields = ['title', 'discipline', 'course_code', 'semester', 'description', 'learning_objectives', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discipline': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'learning_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['curriculum', 'title', 'description', 'assignment_type', 'instructions', 'due_date', 'max_points', 'attachment']
        widgets = {
            'curriculum': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submission_file', 'submission_text']
        widgets = {
            'submission_file': forms.FileInput(attrs={'class': 'form-control'}),
            'submission_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Enter your submission text here...'}),
        }

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['grade', 'feedback']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
