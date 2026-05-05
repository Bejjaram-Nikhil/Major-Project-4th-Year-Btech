from django import forms
from .models import SurveyTemplate, AnalyticalReport

class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyTemplate
        fields = ['title', 'description', 'survey_type', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'survey_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = AnalyticalReport
        fields = ['title', 'report_type', 'description', 'methodology', 'findings', 'recommendations']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'methodology': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
