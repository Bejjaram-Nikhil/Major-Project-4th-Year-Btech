from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .models import Feedback
from .forms import FeedbackForm, FeedbackResponseForm


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback! We will review it shortly.')
            return redirect('feedback:my_feedback')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form})


@login_required
def my_feedback(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'feedback/my_feedback.html', context)


@login_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    
    # Users can only view their own feedback, admins can view all
    if feedback.user != request.user and request.user.role != 'admin':
        messages.error(request, 'You do not have permission to view this feedback.')
        return redirect('feedback:my_feedback')
    
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})


# Admin Views
@login_required
def feedback_list_admin(request):
    # Only admin can access
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can access feedback management.')
        return redirect('accounts:dashboard')
    
    feedbacks = Feedback.objects.all().select_related('user', 'responded_by')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        feedbacks = feedbacks.filter(status=status_filter)
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        feedbacks = feedbacks.filter(category=category_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        feedbacks = feedbacks.filter(priority=priority_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        feedbacks = feedbacks.filter(
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    context = {
        'feedbacks': feedbacks,
        'total_feedbacks': feedbacks.count(),
        'pending_count': Feedback.objects.filter(status='pending').count(),
    }
    
    return render(request, 'feedback/feedback_list_admin.html', context)


@login_required
def feedback_respond(request, pk):
    # Only admin can respond
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can respond to feedback.')
        return redirect('accounts:dashboard')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    
    if request.method == 'POST':
        form = FeedbackResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.responded_by = request.user
            feedback.responded_at = timezone.now()
            feedback.save()
            messages.success(request, f'Response sent to {feedback.user.username}.')
            return redirect('feedback:feedback_detail_admin', pk=feedback.pk)
    else:
        form = FeedbackResponseForm(instance=feedback)
    
    context = {
        'form': form,
        'feedback': feedback,
    }
    return render(request, 'feedback/feedback_respond.html', context)


@login_required
def feedback_detail_admin(request, pk):
    # Only admin can access
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can access this page.')
        return redirect('accounts:dashboard')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    return render(request, 'feedback/feedback_detail_admin.html', {'feedback': feedback})


@login_required
@require_http_methods(["POST"])
def feedback_delete(request, pk):
    # Only admin can delete feedback
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can delete feedback.')
        return redirect('accounts:dashboard')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    
    subject = feedback.subject
    username = feedback.user.username
    feedback.delete()
    
    messages.success(request, f'Feedback "{subject}" from {username} has been deleted successfully.')
    return redirect('feedback:feedback_list_admin')
