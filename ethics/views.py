from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EthicalCaseStudy, DiscussionForum, DiscussionPost, EthicalPrinciple
from .forms import CaseStudyForm, ForumForm, PostForm, PrincipleForm


@login_required
def ethics_home(request):
    # Show all case studies for admin/faculty, only published for students
    if request.user.role in ['faculty', 'researcher', 'admin']:
        case_studies = EthicalCaseStudy.objects.all().order_by('-created_at')[:3]
    else:
        case_studies = EthicalCaseStudy.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    forums = DiscussionForum.objects.filter(is_active=True).order_by('-created_at')[:3]
    principles = EthicalPrinciple.objects.all().order_by('-created_at')[:6]
    
    context = {
        'case_studies': case_studies,
        'forums': forums,
        'principles': principles,
    }
    return render(request, 'ethics/home.html', context)


@login_required
def case_study_list(request):
    # Show all case studies for admin/faculty, only published for students
    if request.user.role in ['faculty', 'researcher', 'admin']:
        case_studies = EthicalCaseStudy.objects.all().order_by('-created_at')
    else:
        case_studies = EthicalCaseStudy.objects.filter(is_published=True).order_by('-created_at')
    
    difficulty_filter = request.GET.get('difficulty')
    if difficulty_filter:
        case_studies = case_studies.filter(difficulty_level=difficulty_filter)
    
    context = {
        'case_studies': case_studies,
    }
    return render(request, 'ethics/case_study_list.html', context)


@login_required
def case_study_detail(request, pk):
    case_study = get_object_or_404(EthicalCaseStudy, pk=pk)
    
    # Check if user has permission to view unpublished case studies
    if not case_study.is_published and request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'This case study is not yet published.')
        return redirect('ethics:case_study_list')
    
    forums = case_study.forums.filter(is_active=True)
    
    context = {
        'case_study': case_study,
        'forums': forums,
    }
    return render(request, 'ethics/case_study_detail.html', context)


@login_required
def case_study_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create case studies.')
        return redirect('ethics:case_study_list')
    
    if request.method == 'POST':
        form = CaseStudyForm(request.POST)
        if form.is_valid():
            case_study = form.save(commit=False)
            case_study.created_by = request.user
            case_study.save()
            messages.success(request, 'Ethical Case Study created successfully!')
            return redirect('ethics:case_study_detail', pk=case_study.pk)
    else:
        form = CaseStudyForm()
    
    return render(request, 'ethics/case_study_form.html', {'form': form})


@login_required
def case_study_edit(request, pk):
    case_study = get_object_or_404(EthicalCaseStudy, pk=pk)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to edit case studies.')
        return redirect('ethics:case_study_detail', pk=pk)
    
    if request.method == 'POST':
        form = CaseStudyForm(request.POST, instance=case_study)
        if form.is_valid():
            form.save()
            messages.success(request, 'Case Study updated successfully!')
            return redirect('ethics:case_study_detail', pk=case_study.pk)
    else:
        form = CaseStudyForm(instance=case_study)
    
    context = {
        'form': form,
        'case_study': case_study,
    }
    return render(request, 'ethics/case_study_form.html', context)


@login_required
def forum_list(request):
    forums = DiscussionForum.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'ethics/forum_list.html', {'forums': forums})


@login_required
def forum_detail(request, pk):
    forum = get_object_or_404(DiscussionForum, pk=pk)
    posts = forum.posts.filter(parent_post__isnull=True).order_by('-created_at')
    
    context = {
        'forum': forum,
        'posts': posts,
    }
    return render(request, 'ethics/forum_detail.html', context)


@login_required
def forum_create(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by = request.user
            forum.save()
            messages.success(request, 'Discussion Forum created successfully!')
            return redirect('ethics:forum_detail', pk=forum.pk)
    else:
        form = ForumForm()
    
    return render(request, 'ethics/forum_form.html', {'form': form})


@login_required
def create_post(request, pk):
    forum = get_object_or_404(DiscussionForum, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.forum = forum
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('ethics:forum_detail', pk=pk)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'forum': forum,
    }
    return render(request, 'ethics/post_form.html', context)


@login_required
def reply_post(request, pk):
    parent_post = get_object_or_404(DiscussionPost, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.forum = parent_post.forum
            reply.author = request.user
            reply.parent_post = parent_post
            reply.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('ethics:forum_detail', pk=parent_post.forum.pk)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'parent_post': parent_post,
    }
    return render(request, 'ethics/reply_form.html', context)


@login_required
def principle_list(request):
    principles = EthicalPrinciple.objects.all().order_by('category', '-created_at')
    
    category_filter = request.GET.get('category')
    if category_filter:
        principles = principles.filter(category=category_filter)
    
    context = {
        'principles': principles,
    }
    return render(request, 'ethics/principle_list.html', context)


@login_required
def principle_detail(request, pk):
    principle = get_object_or_404(EthicalPrinciple, pk=pk)
    return render(request, 'ethics/principle_detail.html', {'principle': principle})


@login_required
def principle_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create ethical principles.')
        return redirect('ethics:principle_list')
    
    if request.method == 'POST':
        form = PrincipleForm(request.POST)
        if form.is_valid():
            principle = form.save(commit=False)
            principle.created_by = request.user
            principle.save()
            messages.success(request, 'Ethical Principle created successfully!')
            return redirect('ethics:principle_detail', pk=principle.pk)
    else:
        form = PrincipleForm()
    
    return render(request, 'ethics/principle_form.html', {'form': form})


@login_required
def principle_edit(request, pk):
    principle = get_object_or_404(EthicalPrinciple, pk=pk)
    
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to edit ethical principles.')
        return redirect('ethics:principle_detail', pk=pk)
    
    if request.method == 'POST':
        form = PrincipleForm(request.POST, instance=principle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ethical Principle updated successfully!')
            return redirect('ethics:principle_detail', pk=principle.pk)
    else:
        form = PrincipleForm(instance=principle)
    
    return render(request, 'ethics/principle_form.html', {'form': form})
