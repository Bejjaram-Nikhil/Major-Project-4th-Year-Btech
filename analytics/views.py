from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.utils import timezone
import json
import numpy as np
from scipy import stats
import pandas as pd

from .models import SurveyTemplate, SurveyResponse, AnalyticalReport, StatisticalTest
from .forms import SurveyForm, ReportForm
from accounts.models import User
from assessments.models import AssessmentAttempt
from ai_literacy.models import StudentProgress

@login_required
def analytics_home(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to access analytics.')
        return redirect('accounts:dashboard')
    
    total_surveys = SurveyTemplate.objects.filter(is_active=True).count()
    total_responses = SurveyResponse.objects.count()
    total_reports = AnalyticalReport.objects.count()
    recent_reports = AnalyticalReport.objects.all().order_by('-generated_at')[:5]
    
    context = {
        'total_surveys': total_surveys,
        'total_responses': total_responses,
        'total_reports': total_reports,
        'recent_reports': recent_reports,
    }
    return render(request, 'analytics/home.html', context)

@login_required
def survey_list(request):
    surveys = SurveyTemplate.objects.filter(is_active=True).order_by('-created_at')
    
    type_filter = request.GET.get('survey_type')
    if type_filter:
        surveys = surveys.filter(survey_type=type_filter)
    
    context = {
        'surveys': surveys,
    }
    return render(request, 'analytics/survey_list.html', context)

@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(SurveyTemplate, pk=pk)
    user_response = None
    
    if request.user.role == 'student':
        try:
            user_response = SurveyResponse.objects.get(survey=survey, respondent=request.user)
        except SurveyResponse.DoesNotExist:
            pass
    
    response_count = survey.responses.count()
    
    context = {
        'survey': survey,
        'user_response': user_response,
        'response_count': response_count,
    }
    return render(request, 'analytics/survey_detail.html', context)

@login_required
def survey_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create surveys.')
        return redirect('analytics:survey_list')
    
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()
            messages.success(request, 'Survey created successfully!')
            return redirect('analytics:survey_detail', pk=survey.pk)
    else:
        form = SurveyForm()
    
    return render(request, 'analytics/survey_form.html', {'form': form})

@login_required
def take_survey(request, pk):
    survey = get_object_or_404(SurveyTemplate, pk=pk)
    
    if SurveyResponse.objects.filter(survey=survey, respondent=request.user).exists():
        messages.warning(request, 'You have already completed this survey.')
        return redirect('analytics:survey_detail', pk=pk)
    
    if request.method == 'POST':
        response_data = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                response_data[key] = value
        
        SurveyResponse.objects.create(
            survey=survey,
            respondent=request.user,
            response_data=response_data
        )
        
        messages.success(request, 'Survey submitted successfully!')
        return redirect('analytics:survey_detail', pk=pk)
    
    return render(request, 'analytics/take_survey.html', {'survey': survey})

@login_required
def survey_responses(request, pk):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to view survey responses.')
        return redirect('analytics:survey_detail', pk=pk)
    
    survey = get_object_or_404(SurveyTemplate, pk=pk)
    responses = survey.responses.all().order_by('-submitted_at')
    
    context = {
        'survey': survey,
        'responses': responses,
    }
    return render(request, 'analytics/survey_responses.html', context)

@login_required
def report_list(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to access reports.')
        return redirect('accounts:dashboard')
    
    reports = AnalyticalReport.objects.all().order_by('-generated_at')
    
    type_filter = request.GET.get('report_type')
    if type_filter:
        reports = reports.filter(report_type=type_filter)
    
    context = {
        'reports': reports,
    }
    return render(request, 'analytics/report_list.html', context)

@login_required
def report_detail(request, pk):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to view reports.')
        return redirect('accounts:dashboard')
    
    report = get_object_or_404(AnalyticalReport, pk=pk)
    statistical_tests = report.statistical_tests.all()
    
    context = {
        'report': report,
        'statistical_tests': statistical_tests,
    }
    return render(request, 'analytics/report_detail.html', context)

@login_required
def report_create(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to create reports.')
        return redirect('analytics:report_list')
    
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.generated_by = request.user
            report.save()
            messages.success(request, 'Report created successfully!')
            return redirect('analytics:report_detail', pk=report.pk)
    else:
        form = ReportForm()
    
    return render(request, 'analytics/report_form.html', {'form': form})

@login_required
def generate_readiness_report(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to generate reports.')
        return redirect('analytics:report_list')
    
    # Collect data for readiness analysis
    students = User.objects.filter(role='student')
    assessment_data = []
    
    for student in students:
        attempts = AssessmentAttempt.objects.filter(student=student, completed_at__isnull=False)
        if attempts.exists():
            avg_score = attempts.aggregate(Avg('score'))['score__avg']
            assessment_data.append({
                'student_id': student.id,
                'gender': student.gender,
                'discipline': student.discipline,
                'avg_score': avg_score,
            })
    
    if len(assessment_data) < 3:
        messages.error(request, 'Insufficient data for statistical analysis. Need at least 3 students with completed assessments.')
        return redirect('analytics:report_list')
    
    df = pd.DataFrame(assessment_data)
    
    # Kruskal-Wallis test for discipline differences
    disciplines = df['discipline'].unique()
    if len(disciplines) >= 2:
        groups = [df[df['discipline'] == d]['avg_score'].values for d in disciplines if len(df[df['discipline'] == d]) > 0]
        groups = [g for g in groups if len(g) > 0]
        
        if len(groups) >= 2:
            h_stat, p_value = stats.kruskal(*groups)
            
            findings = f"""
Readiness Analysis Summary:
- Total Students Analyzed: {len(df)}
- Disciplines: {len(disciplines)}
- Average Readiness Score: {df['avg_score'].mean():.2f}%
- Standard Deviation: {df['avg_score'].std():.2f}

Discipline-wise Performance:
"""
            for discipline in disciplines:
                disc_data = df[df['discipline'] == discipline]
                findings += f"\n{discipline}: Mean = {disc_data['avg_score'].mean():.2f}%, N = {len(disc_data)}"
            
            recommendations = """
Recommendations:
1. Focus intervention programs on disciplines with lower readiness scores
2. Develop discipline-specific AI literacy modules
3. Implement peer mentoring between high and low performing disciplines
4. Conduct follow-up assessments quarterly to track improvement
"""
            
            statistical_data = {
                'total_students': len(df),
                'disciplines': list(disciplines),
                'mean_scores': {d: float(df[df['discipline'] == d]['avg_score'].mean()) for d in disciplines},
                'kruskal_wallis_h': float(h_stat),
                'kruskal_wallis_p': float(p_value),
            }
            
            report = AnalyticalReport.objects.create(
                title=f"AI Readiness Analysis - {timezone.now().strftime('%Y-%m-%d')}",
                report_type='readiness',
                description='Comprehensive analysis of student AI readiness across disciplines',
                methodology='Kruskal-Wallis H-test used to compare readiness scores across multiple disciplines (non-parametric test)',
                findings=findings,
                recommendations=recommendations,
                statistical_data=statistical_data,
                generated_by=request.user
            )
            
            # Create statistical test record
            StatisticalTest.objects.create(
                report=report,
                test_name='Discipline Readiness Comparison',
                test_type='kruskal_wallis',
                variables_tested=f"AI Readiness across {len(disciplines)} disciplines",
                test_statistic=h_stat,
                p_value=p_value,
                significance_level=0.05,
                is_significant=(p_value < 0.05),
                interpretation=f"{'Significant' if p_value < 0.05 else 'No significant'} difference in readiness scores across disciplines (p={p_value:.4f})"
            )
            
            messages.success(request, 'Readiness Report generated successfully!')
            return redirect('analytics:report_detail', pk=report.pk)
    
    messages.error(request, 'Unable to perform statistical analysis. Need data from at least 2 disciplines.')
    return redirect('analytics:report_list')

@login_required
def generate_gender_report(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to generate reports.')
        return redirect('analytics:report_list')
    
    # Collect gender-based data
    students = User.objects.filter(role='student')
    gender_data = []
    
    for student in students:
        attempts = AssessmentAttempt.objects.filter(student=student, completed_at__isnull=False)
        if attempts.exists():
            avg_score = attempts.aggregate(Avg('score'))['score__avg']
            gender_data.append({
                'student_id': student.id,
                'gender': student.gender,
                'avg_score': avg_score,
            })
    
    if len(gender_data) < 3:
        messages.error(request, 'Insufficient data for gender gap analysis.')
        return redirect('analytics:report_list')
    
    df = pd.DataFrame(gender_data)
    
    # Mann-Whitney U test for gender comparison (typically male vs female)
    male_scores = df[df['gender'] == 'male']['avg_score'].values
    female_scores = df[df['gender'] == 'female']['avg_score'].values
    
    if len(male_scores) > 0 and len(female_scores) > 0:
        u_stat, p_value = stats.mannwhitneyu(male_scores, female_scores, alternative='two-sided')
        
        findings = f"""
Gender Gap Analysis Summary:
- Total Students Analyzed: {len(df)}
- Male Students: {len(male_scores)} (Mean Score: {male_scores.mean():.2f}%)
- Female Students: {len(female_scores)} (Mean Score: {female_scores.mean():.2f}%)
- Gender Gap: {abs(male_scores.mean() - female_scores.mean()):.2f} percentage points

Gender Distribution:
"""
        for gender in df['gender'].unique():
            gender_count = len(df[df['gender'] == gender])
            gender_mean = df[df['gender'] == gender]['avg_score'].mean()
            findings += f"\n{gender.title()}: N = {gender_count}, Mean = {gender_mean:.2f}%"
        
        recommendations = """
Recommendations:
1. Implement targeted intervention programs for underrepresented groups
2. Create mentorship programs pairing students across gender groups
3. Develop inclusive learning materials that address diverse perspectives
4. Monitor progress through quarterly assessments
5. Promote role models from all gender groups in AI education
"""
        
        statistical_data = {
            'total_students': len(df),
            'male_count': int(len(male_scores)),
            'female_count': int(len(female_scores)),
            'male_mean': float(male_scores.mean()),
            'female_mean': float(female_scores.mean()),
            'mann_whitney_u': float(u_stat),
            'mann_whitney_p': float(p_value),
        }
        
        report = AnalyticalReport.objects.create(
            title=f"Gender Gap Analysis - {timezone.now().strftime('%Y-%m-%d')}",
            report_type='gender',
            description='Statistical analysis of gender-based differences in AI readiness',
            methodology='Mann-Whitney U-test used to compare readiness scores between gender groups (non-parametric test)',
            findings=findings,
            recommendations=recommendations,
            statistical_data=statistical_data,
            generated_by=request.user
        )
        
        # Create statistical test record
        StatisticalTest.objects.create(
            report=report,
            test_name='Gender Readiness Comparison',
            test_type='mann_whitney',
            variables_tested='AI Readiness: Male vs Female',
            test_statistic=u_stat,
            p_value=p_value,
            significance_level=0.05,
            is_significant=(p_value < 0.05),
            interpretation=f"{'Significant' if p_value < 0.05 else 'No significant'} difference in readiness scores between genders (p={p_value:.4f})"
        )
        
        messages.success(request, 'Gender Gap Report generated successfully!')
        return redirect('analytics:report_detail', pk=report.pk)
    
    messages.error(request, 'Unable to perform gender analysis. Need data from both male and female students.')
    return redirect('analytics:report_list')

@login_required
def generate_discipline_report(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to generate reports.')
        return redirect('analytics:report_list')
    
    # Collect discipline engagement data
    students = User.objects.filter(role='student')
    discipline_data = []
    
    for student in students:
        progress_count = StudentProgress.objects.filter(student=student).count()
        completed_count = StudentProgress.objects.filter(student=student, completed_at__isnull=False).count()
        completion_rate = (completed_count / progress_count * 100) if progress_count > 0 else 0
        
        discipline_data.append({
            'student_id': student.id,
            'discipline': student.discipline,
            'modules_started': progress_count,
            'modules_completed': completed_count,
            'completion_rate': completion_rate,
        })
    
    if len(discipline_data) < 3:
        messages.error(request, 'Insufficient data for discipline analysis.')
        return redirect('analytics:report_list')
    
    df = pd.DataFrame(discipline_data)
    
    # Kruskal-Wallis test for discipline engagement
    disciplines = df['discipline'].unique()
    if len(disciplines) >= 2:
        groups = [df[df['discipline'] == d]['completion_rate'].values for d in disciplines if len(df[df['discipline'] == d]) > 0]
        groups = [g for g in groups if len(g) > 0]
        
        if len(groups) >= 2:
            h_stat, p_value = stats.kruskal(*groups)
            
            findings = f"""
Discipline Engagement Analysis Summary:
- Total Students Analyzed: {len(df)}
- Disciplines: {len(disciplines)}
- Average Completion Rate: {df['completion_rate'].mean():.2f}%
- Total Modules Started: {df['modules_started'].sum()}
- Total Modules Completed: {df['modules_completed'].sum()}

Discipline-wise Engagement:
"""
            for discipline in disciplines:
                disc_data = df[df['discipline'] == discipline]
                findings += f"\n{discipline}:"
                findings += f"\n  - Students: {len(disc_data)}"
                findings += f"\n  - Avg Completion Rate: {disc_data['completion_rate'].mean():.2f}%"
                findings += f"\n  - Total Modules Completed: {disc_data['modules_completed'].sum()}"
            
            recommendations = """
Recommendations:
1. Develop discipline-specific learning pathways
2. Create collaborative projects across disciplines
3. Identify and promote best practices from high-performing disciplines
4. Provide additional support resources for low-engagement disciplines
5. Establish cross-disciplinary learning communities
"""
            
            statistical_data = {
                'total_students': len(df),
                'disciplines': list(disciplines),
                'completion_rates': {d: float(df[df['discipline'] == d]['completion_rate'].mean()) for d in disciplines},
                'kruskal_wallis_h': float(h_stat),
                'kruskal_wallis_p': float(p_value),
            }
            
            report = AnalyticalReport.objects.create(
                title=f"Discipline Engagement Analysis - {timezone.now().strftime('%Y-%m-%d')}",
                report_type='discipline',
                description='Analysis of student engagement patterns across academic disciplines',
                methodology='Kruskal-Wallis H-test used to compare completion rates across disciplines',
                findings=findings,
                recommendations=recommendations,
                statistical_data=statistical_data,
                generated_by=request.user
            )
            
            # Create statistical test record
            StatisticalTest.objects.create(
                report=report,
                test_name='Discipline Engagement Comparison',
                test_type='kruskal_wallis',
                variables_tested=f"Module Completion Rates across {len(disciplines)} disciplines",
                test_statistic=h_stat,
                p_value=p_value,
                significance_level=0.05,
                is_significant=(p_value < 0.05),
                interpretation=f"{'Significant' if p_value < 0.05 else 'No significant'} difference in engagement across disciplines (p={p_value:.4f})"
            )
            
            messages.success(request, 'Discipline Engagement Report generated successfully!')
            return redirect('analytics:report_detail', pk=report.pk)
    
    messages.error(request, 'Unable to perform discipline analysis. Need data from at least 2 disciplines.')
    return redirect('analytics:report_list')

@login_required
def analytics_dashboard(request):
    if request.user.role not in ['faculty', 'researcher', 'admin']:
        messages.error(request, 'You do not have permission to access analytics dashboard.')
        return redirect('accounts:dashboard')
    
    # Overall statistics
    total_students = User.objects.filter(role='student').count()
    total_assessments = AssessmentAttempt.objects.filter(completed_at__isnull=False).count()
    avg_score = AssessmentAttempt.objects.filter(completed_at__isnull=False).aggregate(Avg('score'))['score__avg'] or 0
    
    # Gender distribution
    gender_stats = User.objects.filter(role='student').values('gender').annotate(count=Count('id'))
    
    # Discipline distribution
    discipline_stats = User.objects.filter(role='student').exclude(discipline='').values('discipline').annotate(count=Count('id')).order_by('-count')[:10]
    
    # Recent activity
    recent_attempts = AssessmentAttempt.objects.filter(completed_at__isnull=False).order_by('-completed_at')[:10]
    
    context = {
        'total_students': total_students,
        'total_assessments': total_assessments,
        'avg_score': avg_score,
        'gender_stats': gender_stats,
        'discipline_stats': discipline_stats,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'analytics/dashboard.html', context)
