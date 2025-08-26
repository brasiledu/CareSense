#!/usr/bin/env python
"""
Script para adicionar dados de exemplo para o dashboard de pacientes
Cria pacientes fictícios com múltiplas avaliações para demonstrar a evolução
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append('/Users/eduardovinicius/Faculdade/CareSense/caresense-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caresense_project.settings')
django.setup()

from apps.patients.models import Patient
from apps.assessments.models import (
    Assessment, DigitSpanResult, TMTResult, StroopResult
)
from apps.users.models import User
from django.utils import timezone

def create_sample_patients_with_evolution():
    """Criar pacientes com múltiplas avaliações para mostrar evolução"""
    
    # Garantir que existe um usuário avaliador
    evaluator, created = User.objects.get_or_create(
        username='evaluator_demo',
        defaults={
            'email': 'demo@caresense.com',
            'first_name': 'Avaliador',
            'last_name': 'Demo'
        }
    )
    
    print("🧠 Criando pacientes com dados de evolução...")
    
    # Lista de pacientes fictícios
    patients_data = [
        {
            'name': 'Maria Silva Santos',
            'age_birth': datetime(1950, 3, 15),
            'education': 'GRADUACAO',
            'education_years': 16,
            'trend': 'improving'  # Paciente melhorando
        },
        {
            'name': 'João Carlos Oliveira',
            'age_birth': datetime(1960, 8, 22),
            'education': 'MEDIO',
            'education_years': 11,
            'trend': 'declining'  # Paciente piorando
        },
        {
            'name': 'Ana Paula Costa',
            'age_birth': datetime(1945, 12, 3),
            'education': 'FUNDAMENTAL',
            'education_years': 8,
            'trend': 'stable'  # Paciente estável
        },
        {
            'name': 'Carlos Eduardo Lima',
            'age_birth': datetime(1955, 6, 18),
            'education': 'GRADUACAO',
            'education_years': 18,
            'trend': 'improving'
        },
        {
            'name': 'Rosa Maria Ferreira',
            'age_birth': datetime(1948, 11, 30),
            'education': 'MEDIO',
            'education_years': 11,
            'trend': 'declining'
        },
        {
            'name': 'Pedro Henrique Souza',
            'age_birth': datetime(1958, 4, 12),
            'education': 'FUNDAMENTAL',
            'education_years': 4,
            'trend': 'stable'
        },
        {
            'name': 'Luiza Fernanda Alves',
            'age_birth': datetime(1952, 9, 7),
            'education': 'GRADUACAO',
            'education_years': 15,
            'trend': 'improving'
        },
        {
            'name': 'Roberto Carlos Pereira',
            'age_birth': datetime(1943, 1, 25),
            'education': 'MEDIO',
            'education_years': 11,
            'trend': 'declining'
        }
    ]
    
    created_patients = []
    
    for patient_data in patients_data:
        # Criar ou recuperar paciente
        patient, created = Patient.objects.get_or_create(
            full_name=patient_data['name'],
            defaults={
                'birth_date': patient_data['age_birth'],
                'education_level': patient_data['education'],
                'education_years': patient_data['education_years'],
                'room_number': f"Quarto {random.randint(100, 999)}"
            }
        )
        
        if created:
            print(f"✅ Paciente criado: {patient.full_name}")
        else:
            print(f"ℹ️  Paciente já existe: {patient.full_name}")
        
        created_patients.append((patient, patient_data['trend']))
    
    # Criar múltiplas avaliações para cada paciente
    print("\n📊 Criando avaliações com evolução temporal...")
    
    for patient, trend in created_patients:
        # Criar 3-5 avaliações ao longo dos últimos 6 meses
        num_assessments = random.randint(3, 5)
        
        for i in range(num_assessments):
            # Datas espaçadas nos últimos 6 meses
            days_ago = 180 - (i * 40) - random.randint(0, 20)
            assessment_date = timezone.now() - timedelta(days=days_ago)
            
            # Criar avaliação
            assessment = Assessment.objects.create(
                patient=patient,
                assessor=evaluator,
                status='COMPLETED',
                created_at=assessment_date,
                completed_at=assessment_date + timedelta(hours=2)
            )
            
            # Calcular Z-scores baseados na tendência e tempo
            base_factor = 1.0 if trend == 'improving' else (0.5 if trend == 'stable' else -0.5)
            time_factor = i * 0.3  # Melhoria/piora ao longo do tempo
            
            # Digit Span Results
            if trend == 'improving':
                forward_score = min(9, 4 + i)
                backward_score = min(8, 3 + i) 
                z_score = -1.5 + (i * 0.4) + random.uniform(-0.2, 0.2)
            elif trend == 'declining':
                forward_score = max(2, 6 - i)
                backward_score = max(2, 5 - i)
                z_score = 0.5 - (i * 0.4) + random.uniform(-0.2, 0.2)
            else:  # stable
                forward_score = 5 + random.randint(-1, 1)
                backward_score = 4 + random.randint(-1, 1)
                z_score = random.uniform(-0.5, 0.5)
            
            DigitSpanResult.objects.create(
                assessment=assessment,
                forward_score=forward_score,
                forward_span=forward_score + 1,
                backward_score=backward_score,
                backward_span=backward_score + 1,
                z_score=round(z_score, 2)
            )
            
            # TMT Results
            if trend == 'improving':
                time_a = max(25, 80 - (i * 8))
                time_b = max(60, 180 - (i * 15))
                z_score_a = min(2.0, -1.0 + (i * 0.3))
                z_score_b = min(2.0, -1.2 + (i * 0.4))
            elif trend == 'declining':
                time_a = min(150, 60 + (i * 12))
                time_b = min(300, 120 + (i * 25))
                z_score_a = max(-2.0, 0.5 - (i * 0.3))
                z_score_b = max(-2.0, 0.8 - (i * 0.4))
            else:  # stable
                time_a = 70 + random.randint(-10, 10)
                time_b = 150 + random.randint(-20, 20)
                z_score_a = random.uniform(-0.5, 0.5)
                z_score_b = random.uniform(-0.5, 0.5)
            
            TMTResult.objects.create(
                assessment=assessment,
                time_a_seconds=time_a,
                errors_a=random.randint(0, 2),
                time_b_seconds=time_b,
                errors_b=random.randint(0, 3),
                z_score_a=round(z_score_a, 2),
                z_score_b=round(z_score_b, 2)
            )
            
            # Stroop Results
            if trend == 'improving':
                card3_time = max(60, 120 - (i * 8))
                z_score = min(2.0, -1.0 + (i * 0.3))
            elif trend == 'declining':
                card3_time = min(200, 100 + (i * 15))
                z_score = max(-2.0, 0.5 - (i * 0.3))
            else:  # stable
                card3_time = 100 + random.randint(-15, 15)
                z_score = random.uniform(-0.5, 0.5)
            
            StroopResult.objects.create(
                assessment=assessment,
                card_1_time=30 + random.randint(-5, 5),
                card_1_errors=random.randint(0, 1),
                card_2_time=45 + random.randint(-8, 8),
                card_2_errors=random.randint(0, 2),
                card_3_time=card3_time,
                card_3_errors=random.randint(0, 3),
                z_score=round(z_score, 2)
            )
            
            # Calcular risco final baseado nos Z-scores dos testes
            # Usar média dos Z-scores para determinar risco geral
            avg_z_score = (z_score + z_score_a + z_score_b) / 3
            
            if avg_z_score >= -1.0:
                risk = 'LOW'
            elif avg_z_score >= -1.5:
                risk = 'MODERATE' 
            elif avg_z_score >= -2.0:
                risk = 'HIGH'
            else:
                risk = 'CRITICAL'
            
            assessment.final_risk_score = risk
            assessment.save()
            
        print(f"  ✅ {num_assessments} avaliações criadas para {patient.full_name} (tendência: {trend})")
    
    print(f"\n🎉 Dados de exemplo criados com sucesso!")
    print(f"📊 Total de pacientes: {len(created_patients)}")
    print(f"📋 Total de avaliações: {Assessment.objects.count()}")
    print(f"🧠 Agora você pode visualizar os gráficos no dashboard!")
    print(f"🔗 Acesse: http://127.0.0.1:8000/patients/dashboard/")

if __name__ == '__main__':
    try:
        create_sample_patients_with_evolution()
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        import traceback
        traceback.print_exc()
