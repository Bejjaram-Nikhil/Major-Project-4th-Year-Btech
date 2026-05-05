from django import forms
from django.forms import inlineformset_factory
from .models import ReadinessQuestionnaire, Question, QuestionOption


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = ReadinessQuestionnaire
        fields = ['title', 'description', 'category', 'passing_score', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter questionnaire title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the purpose of this questionnaire'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'passing_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'value': '60'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': 'Questionnaire Title',
            'description': 'Description',
            'category': 'Category',
            'passing_score': 'Passing Score (%)',
            'is_active': 'Active',
        }
        help_texts = {
            'passing_score': 'Minimum percentage required to pass (0-100)',
            'is_active': 'Make this questionnaire available to students',
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'order', 'points']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your question here'
            }),
            'question_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '1'
            }),
        }
        labels = {
            'question_text': 'Question Text',
            'question_type': 'Question Type',
            'order': 'Order',
            'points': 'Points',
        }
        help_texts = {
            'order': 'Order in which this question appears in the questionnaire',
            'points': 'Points awarded for answering this question correctly',
        }


# Formset for Question Options - ONLY option_text and is_correct
QuestionOptionFormSet = inlineformset_factory(
    Question,
    QuestionOption,
    fields=['option_text', 'is_correct'],
    extra=2,
    can_delete=True,
    widgets={
        'option_text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter option text'
        }),
        'is_correct': forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
    },
)


class AssessmentResponseForm(forms.Form):
    """Form for students to submit assessment responses"""
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        for question in questions:
            field_name = f'question_{question.id}'
            
            if question.question_type == 'mcq':
                choices = [(opt.id, opt.option_text) for opt in question.options.all()]
                self.fields[field_name] = forms.ChoiceField(
                    label=question.question_text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=True
                )
            
            elif question.question_type == 'true_false':
                choices = [(opt.id, opt.option_text) for opt in question.options.all()]
                self.fields[field_name] = forms.ChoiceField(
                    label=question.question_text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=True
                )
            
            elif question.question_type == 'rating':
                self.fields[field_name] = forms.IntegerField(
                    label=question.question_text,
                    min_value=1,
                    max_value=5,
                    widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'range'}),
                    required=True
                )
            
            elif question.question_type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=question.question_text,
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                    required=False
                )
