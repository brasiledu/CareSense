from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views import View
from apps.patients.models import Patient
from apps.assessments.models import Assessment, DigitSpanResult, TMTResult, StroopResult
from apps.users.models import User

def home(request):
    """Página inicial do Avivamente"""
    context = {
        'total_patients': Patient.objects.count(),
        'total_assessments': Assessment.objects.count(),
        'pending_assessments': Assessment.objects.filter(status='PENDING').count(),
        'completed_assessments': Assessment.objects.filter(status='COMPLETED').count(),
    }
    return render(request, 'core/home.html', context)

def dashboard(request):
    """Dashboard principal do sistema"""
    recent_patients = Patient.objects.all()[:5]
    recent_assessments = Assessment.objects.select_related('patient', 'assessor').all()[:10]
    
    context = {
        'recent_patients': recent_patients,
        'recent_assessments': recent_assessments,
        'stats': {
            'total_patients': Patient.objects.count(),
            'total_assessments': Assessment.objects.count(),
            'pending_assessments': Assessment.objects.filter(status='PENDING').count(),
            'in_progress_assessments': Assessment.objects.filter(status='IN_PROGRESS').count(),
            'completed_assessments': Assessment.objects.filter(status='COMPLETED').count(),
        }
    }
    return render(request, 'core/dashboard.html', context)

def patient_list(request):
    """Lista de pacientes"""
    search = request.GET.get('search', '')
    patients = Patient.objects.all()
    
    if search:
        patients = patients.filter(
            Q(full_name__icontains=search) | 
            Q(room_number__icontains=search)
        )
    
    context = {
        'patients': patients,
        'search': search
    }
    return render(request, 'core/patient_list.html', context)

def patient_detail(request, patient_id):
    """Detalhes de um paciente"""
    patient = get_object_or_404(Patient, id=patient_id)
    assessments = patient.assessments.all().order_by('-created_at')
    
    context = {
        'patient': patient,
        'assessments': assessments
    }
    return render(request, 'core/patient_detail.html', context)

def assessment_list(request):
    """Lista de avaliações"""
    status_filter = request.GET.get('status', '')
    assessments = Assessment.objects.select_related('patient', 'assessor').all()
    
    if status_filter:
        assessments = assessments.filter(status=status_filter)
    
    context = {
        'assessments': assessments,
        'status_filter': status_filter,
        'status_choices': Assessment.STATUS_CHOICES
    }
    return render(request, 'core/assessment_list.html', context)

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
    return render(request, 'core/assessment_detail.html', context)

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
    return render(request, 'core/start_assessment.html', context)

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
    return render(request, 'core/run_tests.html', context)

def run_digit_span(request, assessment_id):
    """Executar teste Digit Span"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        # Salvar resultados
        forward_score = int(request.POST.get('forward_score', 0))
        forward_span = int(request.POST.get('forward_span', 0))
        backward_score = int(request.POST.get('backward_score', 0))
        backward_span = int(request.POST.get('backward_span', 0))
        
        # Calcular Z-score básico (implementação simplificada)
        total_score = forward_score + backward_score
        age = assessment.patient.age
        education = assessment.patient.education_level
        
        # Fórmula simplificada para Z-score
        expected_score = 10 + (education * 0.2) - ((age - 50) * 0.1)
        z_score = (total_score - expected_score) / 3.0
        
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
        
        messages.success(request, 'Resultado do Digit Span salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'core/digit_span_test.html', context)

def run_tmt(request, assessment_id):
    """Executar teste TMT"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        # Salvar resultados
        time_a = float(request.POST.get('time_a', 0))
        errors_a = int(request.POST.get('errors_a', 0))
        time_b = float(request.POST.get('time_b', 0))
        errors_b = int(request.POST.get('errors_b', 0))
        
        # Calcular Z-scores básicos
        age = assessment.patient.age
        education = assessment.patient.education_level
        
        # Fórmulas simplificadas para Z-scores
        expected_time_a = 30 + (age - 50) * 0.5 - education * 0.5
        expected_time_b = 75 + (age - 50) * 1.2 - education * 1.0
        
        z_score_a = (time_a - expected_time_a) / 15.0
        z_score_b = (time_b - expected_time_b) / 30.0
        
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
        
        messages.success(request, 'Resultado do TMT salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'core/tmt_test.html', context)

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
        
        # Calcular Z-score baseado no tempo de interferência (cartão 3)
        age = assessment.patient.age
        education = assessment.patient.education_level
        
        expected_time_3 = 45 + (age - 50) * 0.8 - education * 0.6
        z_score = (card_3_time - expected_time_3) / 20.0
        
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
        
        messages.success(request, 'Resultado do Stroop salvo com sucesso!')
        return redirect('run_tests', assessment_id=assessment_id)
    
    context = {'assessment': assessment}
    return render(request, 'core/stroop_test.html', context)

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
    
    # Calcular risco global baseado nos Z-scores
    deficits = 0
    
    if assessment.digit_span_result.z_score < -1.5:
        deficits += 1
    
    if assessment.tmt_result.z_score_a < -1.5 or assessment.tmt_result.z_score_b < -1.5:
        deficits += 1
    
    if assessment.stroop_result.z_score < -1.5:
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