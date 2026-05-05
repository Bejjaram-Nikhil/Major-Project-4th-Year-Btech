from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.forms import inlineformset_factory
from django.db.models import Max, Q
from django import forms
from .models import ReadinessQuestionnaire, Question, QuestionOption, AssessmentAttempt, StudentResponse
from .forms import QuestionnaireForm, QuestionForm, QuestionOptionFormSet


# Questionnaire Views
@login_required
def questionnaire_list(request):
    if request.user.role == 'student':
        questionnaires = ReadinessQuestionnaire.objects.filter(is_active=True).order_by('-created_at')
    else:
        questionnaires = ReadinessQuestionnaire.objects.all().order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        questionnaires = questionnaires.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category')
    if category_filter:
        questionnaires = questionnaires.filter(category=category_filter)
    
    context = {
        'questionnaires': questionnaires,
    }
    return render(request, 'assessments/questionnaire_list.html', context)


@login_required
def questionnaire_detail(request, pk):
    questionnaire = get_object_or_404(ReadinessQuestionnaire, pk=pk)
    questions = questionnaire.questions.all().order_by('order')
    
    user_attempts = None
    if request.user.role == 'student':
        user_attempts = AssessmentAttempt.objects.filter(
            student=request.user,
            questionnaire=questionnaire
        ).order_by('-started_at')
    
    context = {
        'questionnaire': questionnaire,
        'questions': questions,
        'user_attempts': user_attempts,
    }
    return render(request, 'assessments/questionnaire_detail.html', context)


@login_required
def questionnaire_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create questionnaires.')
        return redirect('assessments:questionnaire_list')
    
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            questionnaire.created_by = request.user
            questionnaire.save()
            messages.success(request, f'Questionnaire "{questionnaire.title}" created successfully!')
            return redirect('assessments:questionnaire_detail', pk=questionnaire.pk)
    else:
        form = QuestionnaireForm()
    
    context = {
        'form': form,
        'title': 'Create Questionnaire',
        'is_edit': False,
    }
    return render(request, 'assessments/questionnaire_form.html', context)


@login_required
def questionnaire_edit(request, pk):
    if request.user.role not in ['admin', 'faculty', 'researcher']:
        messages.error(request, 'You do not have permission to edit questionnaires.')
        return redirect('assessments:questionnaire_list')
    
    questionnaire = get_object_or_404(ReadinessQuestionnaire, pk=pk)
    
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, instance=questionnaire)
        if form.is_valid():
            form.save()
            messages.success(request, f'Questionnaire "{questionnaire.title}" updated successfully!')
            return redirect('assessments:questionnaire_detail', pk=questionnaire.pk)
    else:
        form = QuestionnaireForm(instance=questionnaire)
    
    context = {
        'form': form,
        'questionnaire': questionnaire,
        'title': 'Edit Questionnaire',
        'is_edit': True,
    }
    return render(request, 'assessments/questionnaire_form.html', context)


@login_required
@require_http_methods(["POST"])
def questionnaire_delete(request, pk):
    if request.user.role not in ['admin', 'faculty', 'researcher']:
        messages.error(request, 'You do not have permission to delete questionnaires.')
        return redirect('assessments:questionnaire_list')
    
    questionnaire = get_object_or_404(ReadinessQuestionnaire, pk=pk)
    title = questionnaire.title
    questionnaire.delete()
    
    messages.success(request, f'Questionnaire "{title}" has been deleted successfully.')
    return redirect('assessments:questionnaire_list')


# Question Views
@login_required
def question_create(request, questionnaire_id):
    questionnaire = get_object_or_404(ReadinessQuestionnaire, pk=questionnaire_id)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create questions.')
        return redirect('assessments:questionnaire_detail', pk=questionnaire_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = QuestionOptionFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.questionnaire = questionnaire
            question.save()
            
            formset.instance = question
            formset.save()
            
            # Update total questions count
            questionnaire.total_questions = questionnaire.questions.count()
            questionnaire.save()
            
            messages.success(request, 'Question added successfully!')
            return redirect('assessments:questionnaire_detail', pk=questionnaire_id)
    else:
        form = QuestionForm()
        formset = QuestionOptionFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'questionnaire': questionnaire,
        'title': 'Add Question',
        'is_edit': False,
    }
    return render(request, 'assessments/question_form.html', context)


@login_required
def question_edit(request, pk):
    if request.user.role not in ['admin', 'faculty', 'researcher']:
        messages.error(request, 'You do not have permission to edit questions.')
        return redirect('accounts:dashboard')
    
    question = get_object_or_404(Question, pk=pk)
    questionnaire = question.questionnaire
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = QuestionOptionFormSet(request.POST, instance=question)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('assessments:questionnaire_detail', pk=questionnaire.pk)
    else:
        form = QuestionForm(instance=question)
        formset = QuestionOptionFormSet(instance=question)
    
    context = {
        'form': form,
        'formset': formset,
        'question': question,
        'questionnaire': questionnaire,
        'title': 'Edit Question',
        'is_edit': True,
    }
    return render(request, 'assessments/question_form.html', context)


@login_required
@require_http_methods(["POST"])
def question_delete(request, pk):
    if request.user.role not in ['admin', 'faculty', 'researcher']:
        messages.error(request, 'You do not have permission to delete questions.')
        return redirect('accounts:dashboard')
    
    question = get_object_or_404(Question, pk=pk)
    questionnaire_pk = question.questionnaire.pk
    question_text = question.question_text
    
    question.delete()
    
    # Update total questions count
    questionnaire = ReadinessQuestionnaire.objects.get(pk=questionnaire_pk)
    questionnaire.total_questions = questionnaire.questions.count()
    questionnaire.save()
    
    messages.success(request, f'Question "{question_text}" has been deleted successfully.')
    return redirect('assessments:questionnaire_detail', pk=questionnaire_pk)


# Student Assessment Views
@login_required
def take_assessment(request, pk):
    if request.user.role != 'student':
        messages.error(request, 'Only students can take assessments.')
        return redirect('assessments:questionnaire_detail', pk=pk)
    
    questionnaire = get_object_or_404(ReadinessQuestionnaire, pk=pk, is_active=True)
    questions = questionnaire.questions.all().order_by('order')
    
    if request.method == 'POST':
        # Create attempt
        attempt = AssessmentAttempt.objects.create(
            student=request.user,
            questionnaire=questionnaire,
            total_points=sum(q.points for q in questions)
        )
        
        score = 0
        
        # Process responses for each question
        for question in questions:
            if question.question_type == 'mcq':
                option_id = request.POST.get(f'question_{question.id}')
                if option_id:
                    option = QuestionOption.objects.get(id=option_id)
                    is_correct = option.is_correct
                    points_earned = question.points if is_correct else 0
                    score += points_earned
                    
                    StudentResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option=option,
                        is_correct=is_correct,
                        points_earned=points_earned
                    )
            
            elif question.question_type == 'true_false':
                option_id = request.POST.get(f'question_{question.id}')
                if option_id:
                    option = QuestionOption.objects.get(id=option_id)
                    is_correct = option.is_correct
                    points_earned = question.points if is_correct else 0
                    score += points_earned
                    
                    StudentResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option=option,
                        is_correct=is_correct,
                        points_earned=points_earned
                    )
            
            elif question.question_type == 'rating':
                rating = request.POST.get(f'question_{question.id}')
                if rating:
                    StudentResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        rating_value=int(rating),
                        points_earned=question.points
                    )
                    score += question.points
            
            elif question.question_type == 'text':
                text_response = request.POST.get(f'question_{question.id}')
                if text_response:
                    StudentResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        text_response=text_response,
                        points_earned=question.points
                    )
                    score += question.points
        
        # Complete the attempt
        attempt.completed_at = timezone.now()
        attempt.score = (score / attempt.total_points * 100) if attempt.total_points > 0 else 0
        attempt.passed = attempt.score >= questionnaire.passing_score
        attempt.save()
        
        messages.success(request, f'Assessment completed! Your score: {attempt.score:.2f}%')
        return redirect('assessments:attempt_detail', pk=attempt.pk)
    
    context = {
        'questionnaire': questionnaire,
        'questions': questions,
    }
    return render(request, 'assessments/take_assessment.html', context)


@login_required
def attempt_detail(request, pk):
    attempt = get_object_or_404(AssessmentAttempt, pk=pk)
    
    # Check permissions
    if request.user.role == 'student' and attempt.student != request.user:
        messages.error(request, 'You do not have permission to view this attempt.')
        return redirect('assessments:questionnaire_list')
    
    responses = attempt.responses.all().select_related('question', 'selected_option').order_by('question__order')
    
    context = {
        'attempt': attempt,
        'responses': responses,
    }
    return render(request, 'assessments/attempt_detail.html', context)


@login_required
def my_attempts(request):
    if request.user.role != 'student':
        messages.error(request, 'This page is only for students.')
        return redirect('accounts:dashboard')
    
    attempts = AssessmentAttempt.objects.filter(student=request.user).select_related('questionnaire').order_by('-started_at')
    
    context = {
        'attempts': attempts,
        'total_attempts': attempts.count(),
        'passed_attempts': attempts.filter(passed=True).count(),
    }
    return render(request, 'assessments/my_attempts.html', context)
