#!/usr/bin/env python
"""
Script simples para criar dados de exemplo sem limpar dados existentes
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
sys.path.append('/Users/eduardovinicius/Faculdade/CareSense/caresense-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caresense_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from apps.patients.models import Patient
from apps.assessments.models import Assessment, DigitSpanResult, TMTResult, StroopResult
from evaluators.models import EvaluatorProfile

User = get_user_model()

print("🚀 Criando dados de exemplo...")

# Criar usuários e avaliadores de exemplo
evaluators_data = [
    {
        'first_name': 'Dr. Ana',
        'last_name': 'Silva',
        'email': 'ana.silva@hospital.com',
        'username': 'ana.silva',
        'crp': '06/12345',
        'specialization': 'Neuropsicologia'
    },
    {
        'first_name': 'Dr. Carlos',
        'last_name': 'Santos',
        'email': 'carlos.santos@hospital.com',
        'username': 'carlos.santos',
        'crp': '06/23456',
        'specialization': 'Psicologia Clínica'
    }
]

print("👨‍⚕️ Criando avaliadores...")
for data in evaluators_data:
    if not User.objects.filter(username=data['username']).exists():
        user = User.objects.create_user(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password='demo123',
            is_staff=True
        )
        
        EvaluatorProfile.objects.create(
            user=user,
            crp_number=data['crp'],
            specialization=data['specialization']
        )
        print(f"   ✅ Criado: {user.get_full_name()}")
    else:
        print(f"   ⏭️ Já existe: {data['username']}")

# Criar pacientes de exemplo
patients_data = [
    {
        'full_name': 'João Silva',
        'birth_date': datetime(1945, 3, 15).date(),
        'education_level': 'FUNDAMENTAL',
        'education_years': 8,
        'room_number': '101A'
    },
    {
        'full_name': 'Maria Santos',
        'birth_date': datetime(1938, 7, 22).date(),
        'education_level': 'MEDIO',
        'education_years': 11,
        'room_number': '102B'
    },
    {
        'full_name': 'Pedro Oliveira',
        'birth_date': datetime(1952, 12, 3).date(),
        'education_level': 'GRADUACAO',
        'education_years': 16,
        'room_number': '103A'
    },
    {
        'full_name': 'Ana Costa',
        'birth_date': datetime(1960, 5, 18).date(),
        'education_level': 'POSGRAD',
        'education_years': 18,
        'room_number': '104C'
    }
]

print("🏥 Criando pacientes...")
created_patients = []
for data in patients_data:
    if not Patient.objects.filter(full_name=data['full_name']).exists():
        patient = Patient.objects.create(**data)
        created_patients.append(patient)
        print(f"   ✅ Criado: {patient.full_name}")
    else:
        patient = Patient.objects.get(full_name=data['full_name'])
        created_patients.append(patient)
        print(f"   ⏭️ Já existe: {patient.full_name}")

# Criar avaliações de exemplo
print("📋 Criando avaliações...")
evaluators = list(EvaluatorProfile.objects.all())

if evaluators:
    for i, patient in enumerate(created_patients):
        # Criar 1-2 avaliações por paciente
        num_assessments = random.randint(1, 2)
        
        for j in range(num_assessments):
            days_ago = random.randint(1, 30)
            created_at = timezone.now() - timedelta(days=days_ago)
            
            if not Assessment.objects.filter(patient=patient, created_at__date=created_at.date()).exists():
                assessment = Assessment.objects.create(
                    patient=patient,
                    assessor=random.choice(evaluators).user,
                    status=random.choice(['COMPLETED', 'COMPLETED', 'PENDING']),  # Mais completas
                    created_at=created_at
                )
                
                # Criar resultados dos testes se a avaliação estiver completa
                if assessment.status == 'COMPLETED':
                    # Digit Span Test
                    forward_score = random.randint(4, 12)
                    backward_score = random.randint(3, 10)
                    
                    DigitSpanResult.objects.create(
                        assessment=assessment,
                        forward_score=forward_score,
                        forward_span=random.randint(4, 8),
                        backward_score=backward_score,
                        backward_span=random.randint(3, 7)
                    )
                    
                    # TMT Test
                    age = patient.age
                    base_tmt_a = 30 + (age - 60) * 0.5 + random.uniform(-5, 10)
                    base_tmt_b = 75 + (age - 60) * 1.2 + random.uniform(-10, 20)
                    
                    TMTResult.objects.create(
                        assessment=assessment,
                        time_a_seconds=round(max(20, base_tmt_a), 1),
                        errors_a=random.randint(0, 2),
                        time_b_seconds=round(max(45, base_tmt_b), 1),
                        errors_b=random.randint(0, 3)
                    )
                    
                    # Stroop Test
                    base_time_1 = 20 + random.uniform(-3, 5)
                    base_time_2 = 18 + random.uniform(-3, 5)
                    base_time_3 = 35 + (age - 60) * 0.3 + random.uniform(-5, 10)
                    
                    StroopResult.objects.create(
                        assessment=assessment,
                        card_1_time=round(base_time_1, 1),
                        card_1_errors=random.randint(0, 1),
                        card_2_time=round(base_time_2, 1),
                        card_2_errors=random.randint(0, 1),
                        card_3_time=round(max(15, base_time_3), 1),
                        card_3_errors=random.randint(0, 2)
                    )
                
                print(f"   ✅ Avaliação criada: {assessment.id} - {patient.full_name}")

print("\n📊 Resumo dos dados criados:")
print(f"   - {User.objects.filter(is_superuser=False).count()} usuários")
print(f"   - {EvaluatorProfile.objects.count()} avaliadores")
print(f"   - {Patient.objects.count()} pacientes")
print(f"   - {Assessment.objects.count()} avaliações")
print(f"   - {DigitSpanResult.objects.count()} resultados Digit Span")
print(f"   - {TMTResult.objects.count()} resultados TMT")
print(f"   - {StroopResult.objects.count()} resultados Stroop")

print("\n✅ Dados de exemplo criados com sucesso!")
print("\n📝 Credenciais de acesso:")
print("   Admin: admin / admin123")
print("   Avaliador 1: ana.silva / demo123")
print("   Avaliador 2: carlos.santos / demo123")
