from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.views import View
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
import json
from apps.core.z_score_utils import normalize_assessment_z_scores, calculate_composite_z_score
from apps.patients.models import Patient
from apps.assessments.models import Assessment, DigitSpanResult, TMTResult, StroopResult, MeemResult, ClockDrawingResult
from apps.assessments.services import score_calculator
from apps.users.models import User
import logging
logger = logging.getLogger(__name__)

def home(request):
    """Página inicial do Avivamente.
    Autenticado -> dashboard; Anônimo -> login.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('evaluators:login')

# Healthcheck simples
def healthz(request):
    return JsonResponse({"status": "ok"})

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
    
    # Dados para gráfico de distribuição por teste (dinâmico)
    test_stats = {
        'digit_span_count': DigitSpanResult.objects.count(),
        'tmt_count': TMTResult.objects.count(),
        'stroop_count': StroopResult.objects.count(),
        'meem_count': MeemResult.objects.count(),
        'clock_count': ClockDrawingResult.objects.count(),
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
    
    # Estatísticas de performance (dinâmicas e normalizadas 0-100)
    # 1) Taxa de conclusão (já dinâmica)
    total_assessments = stats['total_assessments']
    completed_assessments = stats['completed_assessments']
    completion_rate = round((completed_assessments / total_assessments * 100) if total_assessments > 0 else 0)
    
    # 2) Z-score médio final das avaliações concluídas (se existir)
    completed_with_final = Assessment.objects.filter(status='COMPLETED').exclude(final_z_score__isnull=True)
    if completed_with_final.exists():
        avg_final_z = sum(a.final_z_score for a in completed_with_final) / completed_with_final.count()
    else:
        avg_final_z = 0.0
    # Converter z médio para um índice 0-100 simples (centro em 50)
    z_score_index = max(0, min(100, round(50 + (avg_final_z * 10))))
    
    # 3) Índice de tempo médio do TMT (quanto menor o tempo, melhor)
    tmt_qs = TMTResult.objects.all()
    if tmt_qs.exists():
        avg_tmt_time = sum((t.time_a_seconds or 0) + (t.time_b_seconds or 0) for t in tmt_qs) / tmt_qs.count()
        # Normalizar assumindo 180s como referência: 0s -> 100, 180s -> 0
        tmt_time_index = 100 - min(100, round((avg_tmt_time / 180.0) * 100))
    else:
        tmt_time_index = 0
    
    # 4) Acurácia aproximada baseada em erros do TMT (sem erros = 100)
    if tmt_qs.exists():
        no_error_count = sum(1 for t in tmt_qs if (t.errors_a or 0) + (t.errors_b or 0) == 0)
        accuracy = round((no_error_count / tmt_qs.count()) * 100)
    else:
        accuracy = 0
    
    performance_stats = {
        'avg_z_score': z_score_index,
        'completion_rate': completion_rate,
        'avg_time': tmt_time_index,
        'accuracy': accuracy,
    }
    
    context = {
        'stats': stats,
        'test_stats': test_stats,
        'timeline_labels': json.dumps(timeline_labels),
        'timeline_data': json.dumps(timeline_data),
        'age_stats': age_stats,
        'performance_stats': performance_stats,
        # JSON para consumo direto no JS
        'stats_json': json.dumps(stats),
        'test_stats_json': json.dumps(test_stats),
        'age_stats_json': json.dumps(age_stats),
        'performance_stats_json': json.dumps(performance_stats),
        # 'recent_activities': []  # opcional; template já trata quando vazio
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
    return render(request, 'assessments/management/assessment_list.html', context)

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
    return render(request, 'assessments/management/assessment_detail.html', context)

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
    return render(request, 'assessments/management/start_assessment.html', context)

def run_tests(request, assessment_id):
    """Página principal para executar os testes"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Verificar quais testes já foram realizados
    tests_completed = {
        'digit_span': hasattr(assessment, 'digit_span_result'),
        'tmt': hasattr(assessment, 'tmt_result'),
        'stroop': hasattr(assessment, 'stroop_result'),
        'meem': hasattr(assessment, 'meem_result'),
        'clock_drawing': hasattr(assessment, 'clock_drawing_result'),
    }
    
    context = {
        'assessment': assessment,
        'tests_completed': tests_completed,
        'all_completed': all(tests_completed.values()) if tests_completed else False
    }
    return render(request, 'assessments/management/run_tests.html', context)

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
    return render(request, 'assessments/tests/digit_span_test.html', context)

def run_tmt(request, assessment_id):
    """Executar teste TMT"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        # Salvar resultados
        time_a = float(request.POST.get('time_a', 0))
        errors_a = int(request.POST.get('errors_a', 0))
        time_b = float(request.POST.get('time_b', 0))
        errors_b = int(request.POST.get('errors_b', 0))
        
        # Calcular Z-scores usando dados normativos (brutos, sem normalização)
        patient = assessment.patient
        z_score_a, z_score_b = score_calculator.calculate_tmt_z_scores(
            patient, time_a, time_b, errors_a, errors_b
        )
        logger.debug(
            "TMT submission assessment=%s patient_age=%s times=(A:%.2fs,B:%.2fs) errors=(A:%d,B:%d) raw_z=(A:%.3f,B:%.3f)",
            assessment.id, getattr(patient, 'age', None), time_a, time_b, errors_a, errors_b, z_score_a, z_score_b
        )
        
        # Criar ou atualizar resultado (deixar normalização para o model TMTResult.save)
        tmt_result, created = TMTResult.objects.get_or_create(
            assessment=assessment,
            defaults={
                'time_a_seconds': time_a,
                'errors_a': errors_a,
                'time_b_seconds': time_b,
                'errors_b': errors_b
            }
        )
        
        if not created:
            tmt_result.time_a_seconds = time_a
            tmt_result.errors_a = errors_a
            tmt_result.time_b_seconds = time_b
            tmt_result.errors_b = errors_b
        
        # Save dispara cálculo/normalização em TMTResult.save()
        tmt_result.save()
        
        # Atualizar status da avaliação
        assessment.status = 'IN_PROGRESS'
        assessment.save()
        
        messages.success(request, 'Resultado do TMT salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'assessments/tests/tmt_test.html', context)

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
    return render(request, 'assessments/tests/stroop_test.html', context)

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

@login_required
def patients_dashboard(request):
    """Dashboard de evolução de pacientes com análises detalhadas"""
    from django.db.models import Avg, Count, Max, Min
    
    # Filtros
    period = request.GET.get('period', '30')  # 30, 60, 90 dias ou 'all'
    selected_patient_id = request.GET.get('patient', '')  # Filtro por paciente específico
    test_type = request.GET.get('test_type', 'all')  # Filtro por tipo de teste
    
    # Aplicar filtro de período
    if period != 'all':
        cutoff_date = timezone.now().date() - timedelta(days=int(period))
        assessments_query = Assessment.objects.filter(created_at__date__gte=cutoff_date)
    else:
        assessments_query = Assessment.objects.all()
    
    # Aplicar filtro de paciente
    if selected_patient_id:
        try:
            assessments_query = assessments_query.filter(patient_id=int(selected_patient_id))
        except (ValueError, TypeError):
            selected_patient_id = ''
    
    # Estatísticas gerais
    stats = {
        'total_patients': Patient.objects.count(),
        'patients_with_multiple_assessments': Patient.objects.annotate(
            assessment_count=Count('assessments')
        ).filter(assessment_count__gt=1).count(),
        'total_assessments': assessments_query.count(),
        'completed_assessments': assessments_query.filter(status='COMPLETED').count(),
    }
    
    # Análise de evolução por paciente
    patients_evolution = []
    patients_with_multiple = Patient.objects.annotate(
        assessment_count=Count('assessments')
    ).filter(assessment_count__gt=1).prefetch_related('assessments')
    
    for patient in patients_with_multiple:
        assessments = patient.assessments.filter(
            status='COMPLETED'
        ).order_by('created_at')
        
        if assessments.count() < 2:
            continue
            
        # Calcular tendência baseada em Z-scores médios
        first_assessment = assessments.first()
        last_assessment = assessments.last()
        
        first_z_scores = []
        last_z_scores = []
        
        # Calcular médias usando funções utilitárias
        first_normalized = normalize_assessment_z_scores(first_assessment)
        last_normalized = normalize_assessment_z_scores(last_assessment)
        
        if first_normalized and last_normalized:
            first_avg = calculate_composite_z_score(first_normalized)
            last_avg = calculate_composite_z_score(last_normalized)
            improvement = last_avg - first_avg
            
            # Determinar tendência
            if improvement > 0.5:
                trend = 'improving'
                trend_label = 'Melhorando'
                trend_color = '#28a745'
            elif improvement < -0.5:
                trend = 'declining'
                trend_label = 'Piorando'
                trend_color = '#dc3545'
            else:
                trend = 'stable'
                trend_label = 'Estável'
                trend_color = '#ffc107'
            
            patients_evolution.append({
                'patient': patient,
                'first_date': first_assessment.created_at,
                'last_date': last_assessment.created_at,
                'first_avg_z': round(first_avg, 2),
                'last_avg_z': round(last_avg, 2),
                'improvement': round(improvement, 2),
                'trend': trend,
                'trend_label': trend_label,
                'trend_color': trend_color,
                'assessment_count': assessments.count(),
                'days_between': (last_assessment.created_at.date() - first_assessment.created_at.date()).days
            })
    
    # Ordenar por melhoria (maiores melhorias primeiro)
    patients_evolution.sort(key=lambda x: x['improvement'], reverse=True)
    
    # Estatísticas de evolução
    evolution_stats = {
        'improving_count': len([p for p in patients_evolution if p['trend'] == 'improving']),
        'declining_count': len([p for p in patients_evolution if p['trend'] == 'declining']),
        'stable_count': len([p for p in patients_evolution if p['trend'] == 'stable']),
    }
    
    # Dados para gráfico de evolução temporal (média de Z-scores por semana)
    timeline_data = []
    timeline_labels = []
    
    # Dados específicos por teste para gráficos
    test_performance_data = {
        'digit_span': {'labels': [], 'data': []},
        'tmt_a': {'labels': [], 'data': []},
        'tmt_b': {'labels': [], 'data': []},
        'stroop': {'labels': [], 'data': []},
        'meem': {'labels': [], 'data': []},
        'clock_drawing': {'labels': [], 'data': []}
    }
    
    # Calcular médias diárias dos últimos 30 dias
    for day in range(30):
        day_date = timezone.now().date() - timedelta(days=day)
        
        day_assessments = assessments_query.filter(
            status='COMPLETED',
            created_at__date=day_date
        )
        
        day_z_scores = []
        day_test_scores = {
            'digit_span': [],
            'tmt_a': [],
            'tmt_b': [],
            'stroop': [],
            'meem': [],
            'clock_drawing': []
        }
        
        for assessment in day_assessments:
            # Usar função utilitária para normalização consistente
            normalized_scores = normalize_assessment_z_scores(assessment)
            
            # Adicionar todos os scores normalizados
            for test_name, score in normalized_scores.items():
                day_z_scores.append(score)
                day_test_scores[test_name].append(score)
        
        # Calcular médias
        if day_z_scores:
            avg_z_score = sum(day_z_scores) / len(day_z_scores)
        else:
            avg_z_score = 0
        
        timeline_data.insert(0, round(avg_z_score, 2))
        timeline_labels.insert(0, day_date.strftime('%d/%m'))
        
        # Adicionar dados específicos por teste
        for test_name, scores in day_test_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                test_performance_data[test_name]['data'].insert(0, round(avg_score, 2))
            else:
                test_performance_data[test_name]['data'].insert(0, 0)
            test_performance_data[test_name]['labels'].insert(0, day_date.strftime('%d/%m'))
    
    # Estatísticas por teste - usando funções utilitárias para normalização consistente
    from apps.core.z_score_utils import normalize_z_score_for_deficit, get_test_type
    
    test_stats = {}
    completed_assessments = assessments_query.filter(status='COMPLETED')
    
    for test_name in ['digit_span', 'tmt', 'stroop', 'meem', 'clock_drawing']:
        z_scores = []
        
        for assessment in completed_assessments:
            # Usar função utilitária para obter Z-scores normalizados
            normalized_scores = normalize_assessment_z_scores(assessment)
            
            if test_name == 'digit_span' and 'digit_span' in normalized_scores:
                z_scores.append(normalized_scores['digit_span'])
            elif test_name == 'tmt':
                if 'tmt_a' in normalized_scores:
                    z_scores.append(normalized_scores['tmt_a'])
                if 'tmt_b' in normalized_scores:
                    z_scores.append(normalized_scores['tmt_b'])
            elif test_name == 'stroop' and 'stroop' in normalized_scores:
                z_scores.append(normalized_scores['stroop'])
            elif test_name == 'meem' and 'meem' in normalized_scores:
                z_scores.append(normalized_scores['meem'])
            elif test_name == 'clock_drawing' and 'clock_drawing' in normalized_scores:
                z_scores.append(normalized_scores['clock_drawing'])
        
        if z_scores:
            test_stats[test_name] = {
                'count': len(z_scores),
                'avg_z_score': round(sum(z_scores) / len(z_scores), 2),
                'min_z_score': round(min(z_scores), 2),
                'max_z_score': round(max(z_scores), 2),
                'below_normal': len([z for z in z_scores if z < -1.5]),
                'normal': len([z for z in z_scores if -1.5 <= z <= 1.5]),
                'above_normal': len([z for z in z_scores if z > 1.5])
            }
        else:
            test_stats[test_name] = {
                'count': 0, 'avg_z_score': 0, 'min_z_score': 0, 'max_z_score': 0,
                'below_normal': 0, 'normal': 0, 'above_normal': 0
            }
    
    # Lista de pacientes para o filtro
    all_patients = Patient.objects.all().order_by('full_name')
    selected_patient = None
    if selected_patient_id:
        try:
            selected_patient = Patient.objects.get(id=int(selected_patient_id))
        except Patient.DoesNotExist:
            pass
    
    context = {
        'stats': stats,
        'patients_evolution': patients_evolution[:20],  # Top 20
        'evolution_stats': evolution_stats,
        'timeline_data': json.dumps(timeline_data),
        'timeline_labels': json.dumps(timeline_labels),
        'test_performance_data': json.dumps(test_performance_data),
        'test_stats': test_stats,
        'period': period,
        'selected_patient_id': selected_patient_id,
        'selected_patient': selected_patient,
        'test_type': test_type,
        'all_patients': all_patients,
        'improving_patients': [p for p in patients_evolution if p['trend'] == 'improving'][:5],
        'declining_patients': [p for p in patients_evolution if p['trend'] == 'declining'][:5],
    }
    
    return render(request, 'core/patients_dashboard.html', context)

