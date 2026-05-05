from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CurriculumIntegration, Assignment, AssignmentSubmission
from .forms import CurriculumForm, AssignmentForm, SubmissionForm, GradeSubmissionForm

@login_required
def curriculum_list(request):
    curriculums = CurriculumIntegration.objects.filter(is_active=True).order_by('-created_at')
    
    discipline_filter = request.GET.get('discipline')
    if discipline_filter:
        curriculums = curriculums.filter(discipline=discipline_filter)
    
    context = {
        'curriculums': curriculums,
        'disciplines': CurriculumIntegration.objects.values_list('discipline', flat=True).distinct(),
    }
    return render(request, 'curriculum/curriculum_list.html', context)

@login_required
def curriculum_detail(request, pk):
    curriculum = get_object_or_404(CurriculumIntegration, pk=pk)
    assignments = curriculum.assignments.all().order_by('-created_at')
    
    context = {
        'curriculum': curriculum,
        'assignments': assignments,
    }
    return render(request, 'curriculum/curriculum_detail.html', context)

@login_required
def curriculum_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create curriculum integrations.')
        return redirect('curriculum:curriculum_list')
    
    if request.method == 'POST':
        form = CurriculumForm(request.POST)
        if form.is_valid():
            curriculum = form.save(commit=False)
            curriculum.created_by = request.user
            curriculum.save()
            messages.success(request, 'Curriculum Integration created successfully!')
            return redirect('curriculum:curriculum_detail', pk=curriculum.pk)
    else:
        form = CurriculumForm()
    
    return render(request, 'curriculum/curriculum_form.html', {'form': form, 'title': 'Create Curriculum Integration'})

@login_required
def curriculum_edit(request, pk):
    curriculum = get_object_or_404(CurriculumIntegration, pk=pk)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to edit curriculum integrations.')
        return redirect('curriculum:curriculum_detail', pk=pk)
    
    if request.method == 'POST':
        form = CurriculumForm(request.POST, instance=curriculum)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curriculum Integration updated successfully!')
            return redirect('curriculum:curriculum_detail', pk=pk)
    else:
        form = CurriculumForm(instance=curriculum)
    
    return render(request, 'curriculum/curriculum_form.html', {'form': form, 'title': 'Edit Curriculum Integration'})

@login_required
def assignment_list(request):
    if request.user.role == 'student':
        assignments = Assignment.objects.all().order_by('-due_date')
    else:
        assignments = Assignment.objects.all().order_by('-created_at')
    
    context = {
        'assignments': assignments,
    }
    return render(request, 'curriculum/assignment_list.html', context)

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    user_submission = None
    if request.user.role == 'student':
        try:
            user_submission = AssignmentSubmission.objects.get(assignment=assignment, student=request.user)
        except AssignmentSubmission.DoesNotExist:
            pass
    
    context = {
        'assignment': assignment,
        'user_submission': user_submission,
    }
    return render(request, 'curriculum/assignment_detail.html', context)

@login_required
def assignment_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create assignments.')
        return redirect('curriculum:assignment_list')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('curriculum:assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm()
    
    return render(request, 'curriculum/assignment_form.html', {'form': form, 'title': 'Create Assignment'})

@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to edit assignments.')
        return redirect('curriculum:assignment_detail', pk=pk)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('curriculum:assignment_detail', pk=pk)
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(request, 'curriculum/assignment_form.html', {'form': form, 'title': 'Edit Assignment'})

@login_required
def assignment_submit(request, pk):
    if request.user.role != 'student':
        messages.error(request, 'Only students can submit assignments.')
        return redirect('curriculum:assignment_detail', pk=pk)
    
    assignment = get_object_or_404(Assignment, pk=pk)
    
    existing_submission = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('curriculum:submission_detail', pk=submission.pk)
    else:
        form = SubmissionForm(instance=existing_submission)
    
    context = {
        'form': form,
        'assignment': assignment,
        'existing_submission': existing_submission,
    }
    return render(request, 'curriculum/assignment_submit.html', context)

@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(AssignmentSubmission, pk=pk)
    
    if request.user.role == 'student' and submission.student != request.user:
        messages.error(request, 'You do not have permission to view this submission.')
        return redirect('curriculum:assignment_list')
    
    context = {
        'submission': submission,
    }
    return render(request, 'curriculum/submission_detail.html', context)

@login_required
def grade_submission(request, pk):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to grade submissions.')
        return redirect('curriculum:assignment_list')
    
    submission = get_object_or_404(AssignmentSubmission, pk=pk)
    
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            graded_submission = form.save(commit=False)
            graded_submission.graded_by = request.user
            graded_submission.graded_at = timezone.now()
            graded_submission.save()
            messages.success(request, 'Submission graded successfully!')
            return redirect('curriculum:submission_detail', pk=submission.pk)
    else:
        form = GradeSubmissionForm(instance=submission)
    
    context = {
        'form': form,
        'submission': submission,
    }
    return render(request, 'curriculum/grade_submission.html', context)

@login_required
def my_submissions(request):
    if request.user.role != 'student':
        messages.error(request, 'This page is only for students.')
        return redirect('accounts:dashboard')
    
    submissions = AssignmentSubmission.objects.filter(student=request.user).order_by('-submitted_at')
    
    context = {
        'submissions': submissions,
        'total_submissions': submissions.count(),
        'graded_submissions': submissions.filter(grade__isnull=False).count(),
    }
    return render(request, 'curriculum/my_submissions.html', context)
