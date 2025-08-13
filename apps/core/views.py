from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.views import View
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
import json
from apps.patients.models import Patient
from apps.assessments.models import Assessment, DigitSpanResult, TMTResult, StroopResult
from apps.assessments.services import score_calculator
from apps.users.models import User

def home(request):
    """Página inicial do Avivamente"""
    if not request.user.is_authenticated:
        return redirect('evaluators:login')
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_assessments': Assessment.objects.count(),
        'pending_assessments': Assessment.objects.filter(status='PENDING').count(),
        'completed_assessments': Assessment.objects.filter(status='COMPLETED').count(),
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    """Dashboard principal do sistema com gráficos e análises visuais"""
    
    # Estatísticas básicas
    stats = {
        'total_patients': Patient.objects.count(),
        'total_assessments': Assessment.objects.count(),
        'pending_assessments': Assessment.objects.filter(status='PENDING').count(),
        'in_progress_assessments': Assessment.objects.filter(status='IN_PROGRESS').count(),
        'completed_assessments': Assessment.objects.filter(status='COMPLETED').count(),
        'cancelled_assessments': Assessment.objects.filter(status='CANCELLED').count(),
    }
    
    # Dados para gráfico de distribuição por teste
    test_stats = {
        'digit_span_count': DigitSpanResult.objects.count(),
        'tmt_count': TMTResult.objects.count(),
        'stroop_count': StroopResult.objects.count(),
    }
    
    # Dados para gráfico de evolução temporal (últimos 30 dias)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=29)
    
    timeline_data = []
    timeline_labels = []
    
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        day_assessments = Assessment.objects.filter(
            created_at__date=current_date
        ).count()
        timeline_data.append(day_assessments)
        timeline_labels.append(current_date.strftime('%d/%m'))
    
    # Dados para gráfico de distribuição por faixa etária
    # Como age é uma propriedade calculada, precisamos iterar pelos pacientes
    all_patients = Patient.objects.all()
    age_stats = {
        'age_18_30': 0,
        'age_31_45': 0,
        'age_46_60': 0,
        'age_60_plus': 0,
    }
    
    for patient in all_patients:
        age = patient.age
        if 18 <= age <= 30:
            age_stats['age_18_30'] += 1
        elif 31 <= age <= 45:
            age_stats['age_31_45'] += 1
        elif 46 <= age <= 60:
            age_stats['age_46_60'] += 1
        elif age >= 61:
            age_stats['age_60_plus'] += 1
    
    # Dados para gráfico de performance (simulado com dados básicos)
    total_assessments = stats['total_assessments']
    completed_assessments = stats['completed_assessments']
    
    performance_stats = {
        'avg_z_score': 75,  # Simulado
        'completion_rate': round((completed_assessments / total_assessments * 100) if total_assessments > 0 else 0),
        'avg_time': 85,  # Simulado
        'accuracy': 90,  # Simulado
    }
    
    context = {
        'stats': stats,
        'test_stats': test_stats,
        'timeline_labels': json.dumps(timeline_labels),
        'timeline_data': json.dumps(timeline_data),
        'age_stats': age_stats,
        'performance_stats': performance_stats,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def patient_list(request):
    """Lista de pacientes"""
    search = request.GET.get('search', '')
    patients = Patient.objects.all()
    
    if search:
        patients = patients.filter(
            Q(full_name__icontains=search) | 
            Q(room_number__icontains=search)
        )
    
    # Adicionar informações sobre avaliações pendentes para cada paciente
    for patient in patients:
        # Verificar se tem avaliações pendentes ou em andamento
        pending_assessments = patient.assessments.filter(
            status__in=['PENDING', 'IN_PROGRESS']
        )
        patient.has_pending_assessments = pending_assessments.exists()
        
        # Adicionar contadores por status
        patient.pending_assessments_count = patient.assessments.filter(status='PENDING').count()
        patient.in_progress_assessments_count = patient.assessments.filter(status='IN_PROGRESS').count()
        patient.completed_assessments_count = patient.assessments.filter(status='COMPLETED').count()
        patient.cancelled_assessments_count = patient.assessments.filter(status='CANCELLED').count()
    
    # Estatísticas
    total_patients = patients.count()
    patients_without_assessments = patients.filter(assessments__isnull=True).distinct().count()
    active_assessments_count = Assessment.objects.filter(
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
    context = {
        'patients': patients,
        'search': search,
        'active_assessments_count': active_assessments_count,
        'patients_without_assessments': patients_without_assessments,
    }
    return render(request, 'patients/patient_list.html', context)

def patient_detail(request, patient_id):
    """Detalhes de um paciente"""
    patient = get_object_or_404(Patient, id=patient_id)
    assessments = patient.assessments.all().order_by('-created_at')
    
    context = {
        'patient': patient,
        'assessments': assessments
    }
    return render(request, 'patients/patient_detail.html', context)

def assessment_list(request):
    """Lista de avaliações"""
    status_filter = request.GET.get('status', '')
    patient_filter = request.GET.get('patient', '')
    assessments = Assessment.objects.select_related('patient', 'assessor').all()
    
    # Filtrar por status se especificado
    if status_filter:
        assessments = assessments.filter(status=status_filter)
    
    # Filtrar por paciente se especificado
    if patient_filter:
        try:
            patient_id = int(patient_filter)
            assessments = assessments.filter(patient_id=patient_id)
        except (ValueError, TypeError):
            pass
    
    # Obter informações do paciente se filtrado
    selected_patient = None
    if patient_filter:
        try:
            selected_patient = Patient.objects.get(id=int(patient_filter))
        except (Patient.DoesNotExist, ValueError, TypeError):
            pass
    
    # Buscar todos os pacientes para o seletor
    all_patients = Patient.objects.all().order_by('full_name')
    
    context = {
        'assessments': assessments,
        'status_filter': status_filter,
        'patient_filter': patient_filter,
        'selected_patient': selected_patient,
        'all_patients': all_patients,
        'status_choices': Assessment.STATUS_CHOICES
    }
    return render(request, 'assessments/assessment_list.html', context)

def assessment_detail(request, assessment_id):
    """Detalhes de uma avaliação"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Buscar resultados dos testes
    digit_span = None
    tmt_result = None
    stroop_result = None
    
    try:
        digit_span = assessment.digit_span_result
    except:
        pass
    
    try:
        tmt_result = assessment.tmt_result
    except:
        pass
    
    try:
        stroop_result = assessment.stroop_result
    except:
        pass
    
    context = {
        'assessment': assessment,
        'digit_span': digit_span,
        'tmt_result': tmt_result,
        'stroop_result': stroop_result,
    }
    return render(request, 'assessments/assessment_detail.html', context)

class PatientListView(View):
    def get(self, request):
        # Lógica para listar pacientes
        return render(request, 'patient_list.html')

class PatientDetailView(View):
    def get(self, request, patient_id):
        # Lógica para exibir detalhes do paciente
        return render(request, 'patient_detail.html')

class RunDigitSpanView(View):
    def get(self, request):
        # Lógica para apresentar a interface do teste Span de Dígitos
        return render(request, 'run_digit_span_test.html')

class RunTMTView(View):
    def get(self, request):
        # Lógica para apresentar a interface do teste TMT
        return render(request, 'run_tmt_test.html')

class RunStroopView(View):
    def get(self, request):
        # Lógica para apresentar a interface do teste Stroop
        return render(request, 'run_stroop_test.html')

def start_assessment(request):
    """Iniciar uma nova avaliação - selecionar paciente pendente"""
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        print(f"DEBUG: Recebido patient_id: {patient_id}")
        
        if patient_id:
            try:
                patient = get_object_or_404(Patient, id=patient_id)
                print(f"DEBUG: Paciente encontrado: {patient.full_name}")
                
                # Criar nova avaliação
                assessment = Assessment.objects.create(
                    patient=patient,
                    assessor_id=1,  # Por enquanto, usuário fixo - depois implementar autenticação
                    status='IN_PROGRESS'
                )
                print(f"DEBUG: Avaliação criada com ID: {assessment.id}")
                
                messages.success(request, f'Avaliação iniciada para {patient.full_name}')
                print(f"DEBUG: Redirecionando para run_tests com assessment_id: {assessment.id}")
                return redirect('run_tests', assessment_id=assessment.id)
                
            except Exception as e:
                print(f"DEBUG: Erro ao criar avaliação: {e}")
                messages.error(request, f'Erro ao iniciar avaliação: {e}')
        else:
            print("DEBUG: Nenhum patient_id fornecido")
            messages.error(request, 'Nenhum paciente selecionado')
    
    # Buscar apenas pacientes pendentes de avaliação
    from django.utils import timezone
    from datetime import timedelta
    
    # Obter todos os pacientes com suas últimas avaliações
    patients_pending = []
    all_patients = Patient.objects.prefetch_related('assessments').all().order_by('full_name')
    
    for patient in all_patients:
        last_assessment = patient.assessments.first()  # Mais recente
        
        # Considerar pendente se:
        # 1. Nunca foi avaliado OU
        # 2. Última avaliação foi há mais de 7 dias OU  
        # 3. Última avaliação não foi concluída
        
        is_pending = False
        days_since_last = 0
        
        if not last_assessment:
            # Never assessed
            is_pending = True
            days_since_last = 999  # Valor alto para indicar que nunca foi avaliado
        else:
            days_since_last = (timezone.now().date() - last_assessment.created_at.date()).days
            if days_since_last > 7 or last_assessment.status != 'COMPLETED':
                is_pending = True
        
        if is_pending:
            # Adicionar informação extra para o template
            patient.days_since_last_assessment = days_since_last
            patients_pending.append(patient)
    
    context = {
        'patients': patients_pending
    }
    return render(request, 'assessments/start_assessment.html', context)

def run_tests(request, assessment_id):
    """Página principal para executar os testes"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Verificar quais testes já foram realizados
    tests_completed = {
        'digit_span': hasattr(assessment, 'digit_span_result'),
        'tmt': hasattr(assessment, 'tmt_result'),
        'stroop': hasattr(assessment, 'stroop_result'),
    }
    
    context = {
        'assessment': assessment,
        'tests_completed': tests_completed,
        'all_completed': all(tests_completed.values()) if tests_completed else False
    }
    return render(request, 'assessments/run_tests.html', context)

def run_digit_span(request, assessment_id):
    """Executar teste Digit Span"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        # Salvar resultados
        forward_score = int(request.POST.get('forward_score', 0))
        forward_span = int(request.POST.get('forward_span', 0))
        backward_score = int(request.POST.get('backward_score', 0))
        backward_span = int(request.POST.get('backward_span', 0))
        
        # Calcular Z-score usando dados normativos brasileiros
        total_score = forward_score + backward_score
        patient = assessment.patient
        
        # Usar o calculador de Z-score apropriado
        z_score = score_calculator.calculate_digit_span_z_score(patient, total_score)
        
        # Criar ou atualizar resultado
        digit_result, created = DigitSpanResult.objects.get_or_create(
            assessment=assessment,
            defaults={
                'forward_score': forward_score,
                'forward_span': forward_span,
                'backward_score': backward_score,
                'backward_span': backward_span,
                'z_score': round(z_score, 2)
            }
        )
        
        if not created:
            digit_result.forward_score = forward_score
            digit_result.forward_span = forward_span
            digit_result.backward_score = backward_score
            digit_result.backward_span = backward_span
            digit_result.z_score = round(z_score, 2)
            digit_result.save()
        
        # Atualizar status da avaliação
        assessment.status = 'IN_PROGRESS'
        assessment.save()
        
        messages.success(request, 'Resultado do Digit Span salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'assessments/digit_span_test.html', context)

def run_tmt(request, assessment_id):
    """Executar teste TMT"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        # Salvar resultados
        time_a = float(request.POST.get('time_a', 0))
        errors_a = int(request.POST.get('errors_a', 0))
        time_b = float(request.POST.get('time_b', 0))
        errors_b = int(request.POST.get('errors_b', 0))
        
        # Calcular Z-scores usando dados normativos brasileiros
        patient = assessment.patient
        
        # Usar o calculador de Z-score apropriado
        z_score_a, z_score_b = score_calculator.calculate_tmt_z_scores(
            patient, time_a, time_b, errors_a, errors_b
        )
        
        # Criar ou atualizar resultado
        tmt_result, created = TMTResult.objects.get_or_create(
            assessment=assessment,
            defaults={
                'time_a_seconds': time_a,
                'errors_a': errors_a,
                'time_b_seconds': time_b,
                'errors_b': errors_b,
                'z_score_a': round(z_score_a, 2),
                'z_score_b': round(z_score_b, 2)
            }
        )
        
        if not created:
            tmt_result.time_a_seconds = time_a
            tmt_result.errors_a = errors_a
            tmt_result.time_b_seconds = time_b
            tmt_result.errors_b = errors_b
            tmt_result.z_score_a = round(z_score_a, 2)
            tmt_result.z_score_b = round(z_score_b, 2)
            tmt_result.save()
        
        # Atualizar status da avaliação
        assessment.status = 'IN_PROGRESS'
        assessment.save()
        
        messages.success(request, 'Resultado do TMT salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'assessments/tmt_test.html', context)

def run_stroop(request, assessment_id):
    """Executar teste Stroop"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        # Salvar resultados
        card_1_time = float(request.POST.get('card_1_time', 0))
        card_1_errors = int(request.POST.get('card_1_errors', 0))
        card_2_time = float(request.POST.get('card_2_time', 0))
        card_2_errors = int(request.POST.get('card_2_errors', 0))
        card_3_time = float(request.POST.get('card_3_time', 0))
        card_3_errors = int(request.POST.get('card_3_errors', 0))
        
        # Calcular Z-score usando dados normativos brasileiros
        patient = assessment.patient
        # O tempo de interferência é o cartão 3 (card_3_time)
        interference_time = card_3_time
        
        # Usar o calculador de Z-score apropriado
        z_score = score_calculator.calculate_stroop_z_score(patient, interference_time)
        
        # Criar ou atualizar resultado
        stroop_result, created = StroopResult.objects.get_or_create(
            assessment=assessment,
            defaults={
                'card_1_time': card_1_time,
                'card_1_errors': card_1_errors,
                'card_2_time': card_2_time,
                'card_2_errors': card_2_errors,
                'card_3_time': card_3_time,
                'card_3_errors': card_3_errors,
                'z_score': round(z_score, 2)
            }
        )
        
        if not created:
            stroop_result.card_1_time = card_1_time
            stroop_result.card_1_errors = card_1_errors
            stroop_result.card_2_time = card_2_time
            stroop_result.card_2_errors = card_2_errors
            stroop_result.card_3_time = card_3_time
            stroop_result.card_3_errors = card_3_errors
            stroop_result.z_score = round(z_score, 2)
            stroop_result.save()
        
        # Atualizar status da avaliação
        assessment.status = 'IN_PROGRESS'
        assessment.save()
        
        messages.success(request, 'Resultado do Stroop salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'assessments/stroop_test.html', context)

def complete_assessment(request, assessment_id):
    """Finalizar avaliação e calcular risco global"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Verificar se todos os testes foram realizados
    has_digit_span = hasattr(assessment, 'digit_span_result')
    has_tmt = hasattr(assessment, 'tmt_result')
    has_stroop = hasattr(assessment, 'stroop_result')
    
    if not (has_digit_span and has_tmt and has_stroop):
        messages.error(request, 'Todos os testes devem ser realizados antes de finalizar a avaliação.')
        return redirect('run_tests', assessment_id=assessment_id)
    
    # Usar o sistema de cálculo de risco final
    try:
        final_risk = score_calculator.calculate_final_risk_score(assessment_id)
        if final_risk:
            messages.success(request, f'Avaliação finalizada! Nível de risco: {assessment.get_final_risk_score_display()}')
        else:
            messages.warning(request, 'Avaliação finalizada, mas não foi possível calcular o risco final.')
    except Exception as e:
        messages.error(request, f'Erro ao calcular risco final: {str(e)}')
        # Como fallback, usar a lógica anterior
        deficits = 0
        
        if assessment.digit_span_result.z_score and assessment.digit_span_result.z_score < -1.5:
            deficits += 1
        
        if assessment.tmt_result.z_score_a and assessment.tmt_result.z_score_a > 1.5:
            deficits += 1
        if assessment.tmt_result.z_score_b and assessment.tmt_result.z_score_b > 1.5:
            deficits += 1
        
        if assessment.stroop_result.z_score and assessment.stroop_result.z_score > 1.5:
            deficits += 1
        
        # Determinar nível de risco
        if deficits >= 3:
            risk_level = 'CRITICAL'
        elif deficits >= 2:
            risk_level = 'HIGH'
        elif deficits >= 1:
            risk_level = 'MODERATE'
        else:
            risk_level = 'LOW'
        
        # Finalizar avaliação
        assessment.final_risk_score = risk_level
        assessment.mark_completed()
        
        messages.success(request, f'Avaliação finalizada! Nível de risco: {assessment.get_final_risk_score_display()}')
    
    return redirect('assessment_detail', assessment_id=assessment_id)

def patient_history(request, patient_id):
    """Histórico completo do paciente com dashboard de evolução"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Buscar todas as avaliações do paciente, ordenadas por data
    assessments = Assessment.objects.filter(patient=patient).order_by('created_at')
    
    # Preparar dados para gráficos de evolução
    evolution_data = {
        'dates': [],
        'digit_span_scores': [],
        'digit_span_z_scores': [],
        'tmt_a_times': [],
        'tmt_b_times': [],
        'tmt_a_z_scores': [],
        'tmt_b_z_scores': [],
        'stroop_scores': [],
        'stroop_z_scores': [],
        'risk_scores': []
    }
    
    # Estatísticas gerais
    stats = {
        'total_assessments': assessments.count(),
        'completed_assessments': assessments.filter(status='COMPLETED').count(),
        'pending_assessments': assessments.filter(status='PENDING').count(),
        'in_progress_assessments': assessments.filter(status='IN_PROGRESS').count(),
        'latest_risk': None,
        'risk_trend': 'stable'  # 'improving', 'worsening', 'stable'
    }
    
    # Coletar dados para gráficos
    risk_history = []
    for assessment in assessments.filter(status='COMPLETED'):
        evolution_data['dates'].append(assessment.created_at.strftime('%d/%m/%Y'))
        
        # Dados do Digit Span
        if hasattr(assessment, 'digit_span_result'):
            ds = assessment.digit_span_result
            evolution_data['digit_span_scores'].append(ds.total_score if ds.total_score else 0)
            evolution_data['digit_span_z_scores'].append(ds.z_score if ds.z_score else 0)
        else:
            evolution_data['digit_span_scores'].append(0)
            evolution_data['digit_span_z_scores'].append(0)
        
        # Dados do TMT
        if hasattr(assessment, 'tmt_result'):
            tmt = assessment.tmt_result
            evolution_data['tmt_a_times'].append(tmt.time_a if tmt.time_a else 0)
            evolution_data['tmt_b_times'].append(tmt.time_b if tmt.time_b else 0)
            evolution_data['tmt_a_z_scores'].append(tmt.z_score_a if tmt.z_score_a else 0)
            evolution_data['tmt_b_z_scores'].append(tmt.z_score_b if tmt.z_score_b else 0)
        else:
            evolution_data['tmt_a_times'].append(0)
            evolution_data['tmt_b_times'].append(0)
            evolution_data['tmt_a_z_scores'].append(0)
            evolution_data['tmt_b_z_scores'].append(0)
        
        # Dados do Stroop
        if hasattr(assessment, 'stroop_result'):
            stroop = assessment.stroop_result
            evolution_data['stroop_scores'].append(stroop.interference_score if stroop.interference_score else 0)
            evolution_data['stroop_z_scores'].append(stroop.z_score if stroop.z_score else 0)
        else:
            evolution_data['stroop_scores'].append(0)
            evolution_data['stroop_z_scores'].append(0)
        
        # Risco numérico para tendência
        risk_numeric = {'LOW': 1, 'MODERATE': 2, 'HIGH': 3, 'CRITICAL': 4}
        risk_value = risk_numeric.get(assessment.final_risk_score, 0)
        evolution_data['risk_scores'].append(risk_value)
        risk_history.append(risk_value)
    
    # Calcular tendência de risco
    if len(risk_history) >= 2:
        recent_avg = sum(risk_history[-2:]) / 2
        older_avg = sum(risk_history[:-2]) / len(risk_history[:-2]) if len(risk_history) > 2 else recent_avg
        
        if recent_avg < older_avg - 0.3:
            stats['risk_trend'] = 'improving'
        elif recent_avg > older_avg + 0.3:
            stats['risk_trend'] = 'worsening'
    
    # Última avaliação para estatísticas
    latest_assessment = assessments.filter(status='COMPLETED').last()
    if latest_assessment and latest_assessment.final_risk_score:
        stats['latest_risk'] = latest_assessment.final_risk_score
    
    context = {
        'patient': patient,
        'assessments': assessments,
        'evolution_data': evolution_data,
        'stats': stats,
    }
    
    return render(request, 'patients/patient_history.html', context)