from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Assessment, DigitSpanResult, TMTResult, StroopResult, MeemResult, ClockDrawingResult
from .serializers import (
    AssessmentListSerializer, AssessmentDetailSerializer, AssessmentCreateSerializer,
    SubmitDigitSpanSerializer, SubmitTMTSerializer, SubmitStroopSerializer, SubmitMeemSerializer,
    DigitSpanResultSerializer, TMTResultSerializer, StroopResultSerializer, MeemResultSerializer
)
from .services import calculate_final_risk
from .forms import MeemForm

class AssessmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar assessments
    RF03/RF06 - Views e API endpoints
    """
    queryset = Assessment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AssessmentListSerializer
        elif self.action == 'create':
            return AssessmentCreateSerializer
        return AssessmentDetailSerializer
    
    def get_queryset(self):
        """Filtra assessments baseado no usuário logado"""
        queryset = Assessment.objects.select_related('patient', 'assessor')
        
        # Filtros opcionais
        patient_id = self.request.query_params.get('patient_id')
        status_filter = self.request.query_params.get('status')
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Define o assessor como o usuário logado"""
        serializer.save(assessor=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='submit-digit-span')
    def submit_digit_span(self, request, pk=None):
        """
        Endpoint para submeter resultado do teste Digit Span
        POST /api/assessments/<id>/submit-digit-span/
        """
        assessment = self.get_object()
        
        # Verifica se o assessment pertence ao usuário logado
        if assessment.assessor != request.user:
            return Response(
                {'error': 'Você não tem permissão para modificar esta avaliação'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verifica se já existe um resultado
        if hasattr(assessment, 'digit_span_result'):
            return Response(
                {'error': 'Resultado do Digit Span já foi submetido para esta avaliação'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SubmitDigitSpanSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                # Cria o resultado
                digit_span_result = DigitSpanResult.objects.create(
                    assessment=assessment,
                    **serializer.validated_data
                )
                
                # Atualiza status do assessment
                assessment.status = 'IN_PROGRESS'
                assessment.save()
                
                # Calcula pontuação final se todos os testes estiverem completos
                self._check_and_calculate_final_score(assessment)
                
                result_serializer = DigitSpanResultSerializer(digit_span_result)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='submit-tmt')
    def submit_tmt(self, request, pk=None):
        """
        Endpoint para submeter resultado do teste TMT
        POST /api/assessments/<id>/submit-tmt/
        """
        assessment = self.get_object()
        
        if assessment.assessor != request.user:
            return Response(
                {'error': 'Você não tem permissão para modificar esta avaliação'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if hasattr(assessment, 'tmt_result'):
            return Response(
                {'error': 'Resultado do TMT já foi submetido para esta avaliação'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SubmitTMTSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                tmt_result = TMTResult.objects.create(
                    assessment=assessment,
                    **serializer.validated_data
                )
                
                assessment.status = 'IN_PROGRESS'
                assessment.save()
                
                self._check_and_calculate_final_score(assessment)
                
                result_serializer = TMTResultSerializer(tmt_result)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='submit-stroop')
    def submit_stroop(self, request, pk=None):
        """
        Endpoint para submeter resultado do teste Stroop
        POST /api/assessments/<id>/submit-stroop/
        """
        assessment = self.get_object()
        
        if assessment.assessor != request.user:
            return Response(
                {'error': 'Você não tem permissão para modificar esta avaliação'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if hasattr(assessment, 'stroop_result'):
            return Response(
                {'error': 'Resultado do Stroop já foi submetido para esta avaliação'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SubmitStroopSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                stroop_result = StroopResult.objects.create(
                    assessment=assessment,
                    **serializer.validated_data
                )
                
                assessment.status = 'IN_PROGRESS'
                assessment.save()
                
                self._check_and_calculate_final_score(assessment)
                
                result_serializer = StroopResultSerializer(stroop_result)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='submit-meem')
    def submit_meem(self, request, pk=None):
        """
        Endpoint para submeter resultado do teste MEEM
        POST /api/assessments/<id>/submit-meem/
        """
        assessment = self.get_object()
        
        if assessment.assessor != request.user:
            return Response(
                {'error': 'Você não tem permissão para modificar esta avaliação'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if hasattr(assessment, 'meem_result'):
            return Response(
                {'error': 'Resultado do MEEM já foi submetido para esta avaliação'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SubmitMeemSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                meem_result = MeemResult.objects.create(
                    assessment=assessment,
                    **serializer.validated_data
                )
                
                assessment.status = 'IN_PROGRESS'
                assessment.save()
                
                self._check_and_calculate_final_score(assessment)
                
                result_serializer = MeemResultSerializer(meem_result)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _check_and_calculate_final_score(self, assessment):
        """
        Verifica se todos os testes foram completados e calcula a pontuação final
        """
        has_digit_span = hasattr(assessment, 'digit_span_result')
        has_tmt = hasattr(assessment, 'tmt_result')
        has_stroop = hasattr(assessment, 'stroop_result')
        has_meem = hasattr(assessment, 'meem_result')
        
        if has_digit_span and has_tmt and has_stroop and has_meem:
            # Todos os testes completados, calcular pontuação final
            try:
                final_score = calculate_final_risk(assessment.id)
                if final_score:
                    assessment.refresh_from_db()  # Recarrega o objeto atualizado
            except Exception as e:
                # Log do erro, mas não falha a requisição
                print(f"Erro ao calcular pontuação final: {e}")
    
    @action(detail=True, methods=['get'], url_path='results')
    def get_results(self, request, pk=None):
        """
        Endpoint para obter todos os resultados de um assessment
        GET /api/assessments/<id>/results/
        """
        assessment = self.get_object()
        
        results = {}
        
        if hasattr(assessment, 'digit_span_result'):
            results['digit_span'] = DigitSpanResultSerializer(assessment.digit_span_result).data
        
        if hasattr(assessment, 'tmt_result'):
            results['tmt'] = TMTResultSerializer(assessment.tmt_result).data
        
        if hasattr(assessment, 'stroop_result'):
            results['stroop'] = StroopResultSerializer(assessment.stroop_result).data
        
        if hasattr(assessment, 'meem_result'):
            results['meem'] = MeemResultSerializer(assessment.meem_result).data
        
        return Response({
            'assessment_id': assessment.id,
            'status': assessment.status,
            'final_risk_score': assessment.final_risk_score,
            'results': results
        })
    
    @action(detail=True, methods=['post'], url_path='recalculate-score')
    def recalculate_score(self, request, pk=None):
        """
        Endpoint para recalcular a pontuação final
        POST /api/assessments/<id>/recalculate-score/
        """
        assessment = self.get_object()
        
        if assessment.assessor != request.user:
            return Response(
                {'error': 'Você não tem permissão para modificar esta avaliação'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            final_score = calculate_final_risk(assessment.id)
            assessment.refresh_from_db()
            
            return Response({
                'message': 'Pontuação recalculada com sucesso',
                'final_risk_score': assessment.final_risk_score,
                'status': assessment.status
            })
        except Exception as e:
            return Response(
                {'error': f'Erro ao recalcular pontuação: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

@login_required
def meem_test_view(request, assessment_id):
    """
    View para aplicação do teste MEEM
    """
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Verificar se o usuário tem permissão
    if assessment.assessor != request.user:
        messages.error(request, 'Você não tem permissão para acessar esta avaliação.')
        return redirect('assessment_list')
    
    # Verificar se já existe resultado MEEM
    if hasattr(assessment, 'meem_result'):
        messages.info(request, 'O teste MEEM já foi aplicado nesta avaliação.')
        return redirect('run_tests', assessment_id=assessment.id)
    
    if request.method == 'POST':
        form = MeemForm(request.POST)
        if form.is_valid():
            # Criar resultado MEEM
            meem_result = form.save(commit=False)
            meem_result.assessment = assessment
            meem_result.save()
            
            # Calcular Z-score usando dados normativos brasileiros
            from .services import score_calculator
            patient = assessment.patient
            total_score = meem_result.total_score
            z_score = score_calculator.calculate_meem_z_score(patient, total_score)
            
            # Atualizar resultado com z-score
            meem_result.z_score = round(z_score, 2)
            meem_result.save()
            
            # Atualizar status do assessment
            assessment.status = 'IN_PROGRESS'
            assessment.save()
            
            messages.success(request, 'Teste MEEM aplicado com sucesso!')
            return redirect('run_tests', assessment_id=assessment.id)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = MeemForm()
    
    context = {
        'assessment': assessment,
        'form': form,
        'patient': assessment.patient,
    }
    
    return render(request, 'assessments/tests/meem_test.html', context)

@login_required
def clock_drawing_test_view(request, assessment_id):
    """
    View para aplicação do Teste do Relógio (Clock Drawing Test)
    """
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Verificar se o usuário tem permissão
    if assessment.assessor != request.user:
        messages.error(request, 'Você não tem permissão para acessar esta avaliação.')
        return redirect('assessment_list')
    
    # Verificar se já existe resultado do Clock Drawing Test
    if hasattr(assessment, 'clock_drawing_result'):
        messages.info(request, 'O Teste do Relógio já foi aplicado nesta avaliação.')
        return redirect('run_tests', assessment_id=assessment.id)
    
    if request.method == 'POST':
        from .forms import ClockDrawingForm
        form = ClockDrawingForm(request.POST)
        if form.is_valid():
            # Criar resultado do Clock Drawing Test
            clock_result = form.save(commit=False)
            clock_result.assessment = assessment
            clock_result.save()
            
            # Calcular Z-score usando dados normativos
            from .services import score_calculator
            patient = assessment.patient
            total_score = clock_result.total_score
            z_score = score_calculator.calculate_clock_drawing_z_score(patient, total_score)
            
            # Atualizar resultado com z-score
            clock_result.z_score = round(z_score, 2)
            clock_result.save()
            
            # Atualizar status do assessment
            assessment.status = 'IN_PROGRESS'
            assessment.save()
            
            messages.success(request, 'Teste do Relógio aplicado com sucesso!')
            return redirect('run_tests', assessment_id=assessment.id)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        from .forms import ClockDrawingForm
        form = ClockDrawingForm()
    
    context = {
        'assessment': assessment,
        'form': form,
        'patient': assessment.patient,
    }
    
    return render(request, 'assessments/tests/clock_drawing_test.html', context)