from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AILiteracyFramework, LearningModule, StudentProgress
from .forms import AILiteracyFrameworkForm, LearningModuleForm

@login_required
def framework_list(request):
    frameworks = AILiteracyFramework.objects.filter(is_active=True).order_by('-created_at')
    
    discipline_filter = request.GET.get('discipline')
    if discipline_filter:
        frameworks = frameworks.filter(discipline=discipline_filter)
    
    context = {
        'frameworks': frameworks,
        'disciplines': AILiteracyFramework.objects.values_list('discipline', flat=True).distinct(),
    }
    return render(request, 'ai_literacy/framework_list.html', context)

@login_required
def framework_detail(request, pk):
    framework = get_object_or_404(AILiteracyFramework, pk=pk)
    modules = framework.modules.all().order_by('order')
    
    if request.user.role == 'student':
        progress_data = []
        for module in modules:
            try:
                progress = StudentProgress.objects.get(student=request.user, module=module)
                progress_data.append({
                    'module': module,
                    'progress': progress,
                })
            except StudentProgress.DoesNotExist:
                progress_data.append({
                    'module': module,
                    'progress': None,
                })
        context = {
            'framework': framework,
            'progress_data': progress_data,
        }
    else:
        context = {
            'framework': framework,
            'modules': modules,
        }
    
    return render(request, 'ai_literacy/framework_detail.html', context)

@login_required
def framework_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create frameworks.')
        return redirect('ai_literacy:framework_list')
    
    if request.method == 'POST':
        form = AILiteracyFrameworkForm(request.POST)
        if form.is_valid():
            framework = form.save(commit=False)
            framework.created_by = request.user
            framework.save()
            messages.success(request, 'AI Literacy Framework created successfully!')
            return redirect('ai_literacy:framework_detail', pk=framework.pk)
    else:
        form = AILiteracyFrameworkForm()
    
    return render(request, 'ai_literacy/framework_form.html', {'form': form, 'title': 'Create Framework'})

@login_required
def framework_edit(request, pk):
    framework = get_object_or_404(AILiteracyFramework, pk=pk)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to edit frameworks.')
        return redirect('ai_literacy:framework_detail', pk=pk)
    
    if request.method == 'POST':
        form = AILiteracyFrameworkForm(request.POST, instance=framework)
        if form.is_valid():
            form.save()
            messages.success(request, 'Framework updated successfully!')
            return redirect('ai_literacy:framework_detail', pk=pk)
    else:
        form = AILiteracyFrameworkForm(instance=framework)
    
    return render(request, 'ai_literacy/framework_form.html', {'form': form, 'title': 'Edit Framework'})

@login_required
def framework_delete(request, pk):
    framework = get_object_or_404(AILiteracyFramework, pk=pk)
    
    if request.user.role not in ['admin']:
        messages.error(request, 'You do not have permission to delete frameworks.')
        return redirect('ai_literacy:framework_detail', pk=pk)
    
    if request.method == 'POST':
        framework.delete()
        messages.success(request, 'Framework deleted successfully!')
        return redirect('ai_literacy:framework_list')
    
    return render(request, 'ai_literacy/framework_confirm_delete.html', {'framework': framework})

@login_required
def module_list(request):
    modules = LearningModule.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'ai_literacy/module_list.html', {'modules': modules})

@login_required
def module_detail(request, pk):
    module = get_object_or_404(LearningModule, pk=pk)
    
    progress = None
    if request.user.role == 'student':
        progress, created = StudentProgress.objects.get_or_create(
            student=request.user,
            module=module
        )
    
    return render(request, 'ai_literacy/module_detail.html', {'module': module, 'progress': progress})

@login_required
def module_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create modules.')
        return redirect('ai_literacy:module_list')
    
    if request.method == 'POST':
        form = LearningModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save()
            messages.success(request, 'Learning Module created successfully!')
            return redirect('ai_literacy:module_detail', pk=module.pk)
    else:
        form = LearningModuleForm()
    
    return render(request, 'ai_literacy/module_form.html', {'form': form, 'title': 'Create Module'})

@login_required
def module_edit(request, pk):
    module = get_object_or_404(LearningModule, pk=pk)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to edit modules.')
        return redirect('ai_literacy:module_detail', pk=pk)
    
    if request.method == 'POST':
        form = LearningModuleForm(request.POST, request.FILES, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module updated successfully!')
            return redirect('ai_literacy:module_detail', pk=pk)
    else:
        form = LearningModuleForm(instance=module)
    
    return render(request, 'ai_literacy/module_form.html', {'form': form, 'title': 'Edit Module'})

@login_required
def module_delete(request, pk):
    module = get_object_or_404(LearningModule, pk=pk)
    
    if request.user.role not in ['admin']:
        messages.error(request, 'You do not have permission to delete modules.')
        return redirect('ai_literacy:module_detail', pk=pk)
    
    if request.method == 'POST':
        framework_pk = module.framework.pk
        module.delete()
        messages.success(request, 'Module deleted successfully!')
        return redirect('ai_literacy:framework_detail', pk=framework_pk)
    
    return render(request, 'ai_literacy/module_confirm_delete.html', {'module': module})

@login_required
def module_start(request, pk):
    if request.user.role != 'student':
        messages.error(request, 'Only students can start modules.')
        return redirect('ai_literacy:module_detail', pk=pk)
    
    module = get_object_or_404(LearningModule, pk=pk)
    progress, created = StudentProgress.objects.get_or_create(
        student=request.user,
        module=module
    )
    
    messages.success(request, f'Started learning: {module.title}')
    return redirect('ai_literacy:module_detail', pk=pk)

@login_required
def module_complete(request, pk):
    if request.user.role != 'student':
        messages.error(request, 'Only students can complete modules.')
        return redirect('ai_literacy:module_detail', pk=pk)
    
    module = get_object_or_404(LearningModule, pk=pk)
    progress = get_object_or_404(StudentProgress, student=request.user, module=module)
    
    progress.completed_at = timezone.now()
    progress.progress_percentage = 100
    progress.save()
    
    messages.success(request, f'Congratulations! You completed: {module.title}')
    return redirect('ai_literacy:module_detail', pk=pk)

@login_required
def my_progress(request):
    if request.user.role != 'student':
        messages.error(request, 'This page is only for students.')
        return redirect('accounts:dashboard')
    
    progress = StudentProgress.objects.filter(student=request.user).order_by('-started_at')
    
    total_started = progress.count()
    total_completed = progress.filter(completed_at__isnull=False).count()
    completion_rate = (total_completed / total_started * 100) if total_started > 0 else 0
    
    context = {
        'progress_list': progress,
        'total_started': total_started,
        'total_completed': total_completed,
        'completion_rate': completion_rate,
    }
    return render(request, 'ai_literacy/my_progress.html', context)
