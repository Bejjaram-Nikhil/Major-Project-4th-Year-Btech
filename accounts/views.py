from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count, Avg
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
    }
    
    # Add role-specific data
    if user.role == 'student':
        from ai_literacy.models import StudentProgress
        from assessments.models import AssessmentAttempt
        from curriculum.models import AssignmentSubmission
        
        context['modules_started'] = StudentProgress.objects.filter(student=user).count()
        context['modules_completed'] = StudentProgress.objects.filter(
            student=user, 
            completed_at__isnull=False
        ).count()
        context['assessments_taken'] = AssessmentAttempt.objects.filter(student=user).count()
        context['assignments_submitted'] = AssignmentSubmission.objects.filter(student=user).count()
        
        # Recent progress
        context['recent_progress'] = StudentProgress.objects.filter(
            student=user
        ).select_related('module').order_by('-started_at')[:5]
        
        # Recent attempts
        context['recent_attempts'] = AssessmentAttempt.objects.filter(
            student=user
        ).select_related('questionnaire').order_by('-completed_at')[:5]
        
    elif user.role in ['faculty', 'researcher', 'admin']:
        from ai_literacy.models import AILiteracyFramework, LearningModule
        from assessments.models import ReadinessQuestionnaire
        from curriculum.models import CurriculumIntegration
        
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_frameworks'] = AILiteracyFramework.objects.count()
        context['total_modules'] = LearningModule.objects.count()
        context['total_assessments'] = ReadinessQuestionnaire.objects.count()
        context['total_curriculum'] = CurriculumIntegration.objects.count()
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'profile_user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


# Admin ONLY Views - User Management
@login_required
def user_list(request):
    # ONLY ADMIN can view user list
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can manage users.')
        return redirect('accounts:dashboard')
    
    users = User.objects.all().order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filter by role
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'total_users': users.count(),
    }
    
    return render(request, 'accounts/user_list.html', context)


@login_required
def user_detail(request, pk):
    # ONLY ADMIN can view user details
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can view user details.')
        return redirect('accounts:dashboard')
    
    profile_user = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'profile_user': profile_user})


@login_required
def edit_user(request, pk):
    # ONLY ADMIN can edit users
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can edit users.')
        return redirect('accounts:dashboard')
    
    user_to_edit = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_to_edit.username} updated successfully!')
            return redirect('accounts:user_detail', pk=user_to_edit.pk)
    else:
        form = UserUpdateForm(instance=user_to_edit)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile_user': user_to_edit
    })


@login_required
@require_http_methods(["POST"])
def delete_user(request, pk):
    # ONLY ADMIN can delete users
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can delete users.')
        return redirect('accounts:dashboard')
    
    user_to_delete = get_object_or_404(User, pk=pk)
    
    # Prevent admin from deleting themselves
    if user_to_delete == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('accounts:user_list')
    
    username = user_to_delete.username
    user_to_delete.delete()
    messages.success(request, f'User "{username}" has been deleted successfully.')
    return redirect('accounts:user_list')


@login_required
@require_http_methods(["POST"])
def toggle_verify_user(request, pk):
    # ONLY ADMIN can verify users
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can verify users.')
        return redirect('accounts:dashboard')
    
    user_to_verify = get_object_or_404(User, pk=pk)
    
    # Toggle verification status
    user_to_verify.is_verified = not user_to_verify.is_verified
    user_to_verify.save()
    
    status = "verified" if user_to_verify.is_verified else "unverified"
    messages.success(request, f'User "{user_to_verify.username}" has been {status}.')
    
    # Redirect back to the page they came from
    return redirect(request.META.get('HTTP_REFERER', 'accounts:user_list'))


# Custom Password Change View
class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Your password was successfully updated!"
