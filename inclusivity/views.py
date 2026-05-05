from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InterventionProgram, MentorshipProgram, MentorshipEnrollment, SupportResource
from .forms import InterventionForm, MentorshipForm, EnrollmentForm, ResourceForm

@login_required
def inclusivity_home(request):
    interventions = InterventionProgram.objects.filter(is_active=True).order_by('-created_at')[:3]
    mentorships = MentorshipProgram.objects.filter(is_accepting=True).order_by('-created_at')[:3]
    resources = SupportResource.objects.all().order_by('-created_at')[:6]
    
    context = {
        'interventions': interventions,
        'mentorships': mentorships,
        'resources': resources,
    }
    return render(request, 'inclusivity/home.html', context)

@login_required
def intervention_list(request):
    interventions = InterventionProgram.objects.filter(is_active=True).order_by('-created_at')
    
    target_filter = request.GET.get('target_group')
    if target_filter:
        interventions = interventions.filter(target_group=target_filter)
    
    context = {
        'interventions': interventions,
    }
    return render(request, 'inclusivity/intervention_list.html', context)

@login_required
def intervention_detail(request, pk):
    intervention = get_object_or_404(InterventionProgram, pk=pk)
    return render(request, 'inclusivity/intervention_detail.html', {'intervention': intervention})

@login_required
def intervention_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create intervention programs.')
        return redirect('inclusivity:intervention_list')
    
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.coordinator = request.user
            intervention.save()
            messages.success(request, 'Intervention Program created successfully!')
            return redirect('inclusivity:intervention_detail', pk=intervention.pk)
    else:
        form = InterventionForm()
    
    return render(request, 'inclusivity/intervention_form.html', {'form': form})

@login_required
def mentorship_list(request):
    mentorships = MentorshipProgram.objects.filter(is_accepting=True).order_by('-created_at')
    
    discipline_filter = request.GET.get('discipline')
    if discipline_filter:
        mentorships = mentorships.filter(discipline=discipline_filter)
    
    context = {
        'mentorships': mentorships,
    }
    return render(request, 'inclusivity/mentorship_list.html', context)

@login_required
def mentorship_detail(request, pk):
    mentorship = get_object_or_404(MentorshipProgram, pk=pk)
    enrollments = mentorship.enrollments.filter(status='active')
    
    user_enrolled = False
    if request.user.role == 'student':
        user_enrolled = MentorshipEnrollment.objects.filter(program=mentorship, mentee=request.user).exists()
    
    context = {
        'mentorship': mentorship,
        'enrollments': enrollments,
        'user_enrolled': user_enrolled,
    }
    return render(request, 'inclusivity/mentorship_detail.html', context)

@login_required
def mentorship_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create mentorship programs.')
        return redirect('inclusivity:mentorship_list')
    
    if request.method == 'POST':
        form = MentorshipForm(request.POST)
        if form.is_valid():
            mentorship = form.save(commit=False)
            mentorship.mentor = request.user
            mentorship.save()
            messages.success(request, 'Mentorship Program created successfully!')
            return redirect('inclusivity:mentorship_detail', pk=mentorship.pk)
    else:
        form = MentorshipForm()
    
    return render(request, 'inclusivity/mentorship_form.html', {'form': form})

@login_required
def mentorship_enroll(request, pk):
    if request.user.role != 'student':
        messages.error(request, 'Only students can enroll in mentorship programs.')
        return redirect('inclusivity:mentorship_detail', pk=pk)
    
    mentorship = get_object_or_404(MentorshipProgram, pk=pk)
    
    if MentorshipEnrollment.objects.filter(program=mentorship, mentee=request.user).exists():
        messages.warning(request, 'You are already enrolled in this program.')
        return redirect('inclusivity:mentorship_detail', pk=pk)
    
    if mentorship.current_mentees >= mentorship.max_mentees:
        messages.error(request, 'This mentorship program is full.')
        return redirect('inclusivity:mentorship_detail', pk=pk)
    
    MentorshipEnrollment.objects.create(program=mentorship, mentee=request.user)
    mentorship.current_mentees += 1
    if mentorship.current_mentees >= mentorship.max_mentees:
        mentorship.is_accepting = False
    mentorship.save()
    
    messages.success(request, 'Successfully enrolled in mentorship program!')
    return redirect('inclusivity:mentorship_detail', pk=pk)

@login_required
def my_mentorships(request):
    if request.user.role == 'student':
        enrollments = MentorshipEnrollment.objects.filter(mentee=request.user).order_by('-enrolled_at')
        context = {'enrollments': enrollments}
        return render(request, 'inclusivity/my_mentorships.html', context)
    else:
        programs = MentorshipProgram.objects.filter(mentor=request.user).order_by('-created_at')
        context = {'programs': programs}
        return render(request, 'inclusivity/mentor_programs.html', context)

@login_required
def resource_list(request):
    resources = SupportResource.objects.all().order_by('-created_at')
    
    type_filter = request.GET.get('resource_type')
    if type_filter:
        resources = resources.filter(resource_type=type_filter)
    
    context = {
        'resources': resources,
    }
    return render(request, 'inclusivity/resource_list.html', context)

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(SupportResource, pk=pk)
    return render(request, 'inclusivity/resource_detail.html', {'resource': resource})

@login_required
def resource_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create resources.')
        return redirect('inclusivity:resource_list')
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            messages.success(request, 'Support Resource created successfully!')
            return redirect('inclusivity:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    
    return render(request, 'inclusivity/resource_form.html', {'form': form})
