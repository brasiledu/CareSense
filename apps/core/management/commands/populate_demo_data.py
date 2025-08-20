from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from apps.patients.models import Patient
from apps.assessments.models import Assessment, DigitSpanResult, TMTResult, StroopResult
from evaluators.models import EvaluatorProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o banco com dados de exemplo para demonstração'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Remove todos os dados antes de criar novos'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Removendo dados existentes...')
            Assessment.objects.all().delete()
            Patient.objects.all().delete()
            EvaluatorProfile.objects.filter(user__is_superuser=False).delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Criando dados de exemplo...')
        
        # Criar usuários e avaliadores
        self.create_evaluators()
        
        # Criar pacientes
        patients = self.create_patients()
        
        # Criar avaliações
        self.create_assessments(patients)
        
        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )

    def create_evaluators(self):
        """Cria avaliadores de exemplo"""
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
            },
            {
                'first_name': 'Dra. Maria',
                'last_name': 'Oliveira',
                'email': 'maria.oliveira@hospital.com',
                'username': 'maria.oliveira',
                'crp': '06/34567',
                'specialization': 'Reabilitação Cognitiva'
            }
        ]
        
        for data in evaluators_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_staff': True
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
            
            evaluator, created = EvaluatorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'crp_number': data['crp'],
                    'specialization': data['specialization']
                }
            )
            
            if created:
                self.stdout.write(f'Avaliador criado: {evaluator.user.get_full_name()}')

    def create_patients(self):
        """Cria pacientes de exemplo"""
        patients_data = [
            {
                'full_name': 'João Silva',
                'birth_date': datetime(1945, 3, 15).date(),
                'education_level': 'FUNDAMENTAL',
                'education_years': 8,
                'room_number': '101A',
            },
            {
                'full_name': 'Maria Santos',
                'birth_date': datetime(1938, 7, 22).date(),
                'education_level': 'MEDIO',
                'education_years': 11,
                'room_number': '102B',
            },
            {
                'full_name': 'Pedro Oliveira',
                'birth_date': datetime(1952, 12, 3).date(),
                'education_level': 'GRADUACAO',
                'education_years': 16,
                'room_number': '103A',
            },
            {
                'full_name': 'Ana Costa',
                'birth_date': datetime(1960, 5, 18).date(),
                'education_level': 'POSGRAD',
                'education_years': 18,
                'room_number': '104C',
            },
            {
                'full_name': 'Carlos Ferreira',
                'birth_date': datetime(1948, 9, 12).date(),
                'education_level': 'FUNDAMENTAL',
                'education_years': 6,
                'room_number': '105A',
            },
            {
                'full_name': 'Rosa Lima',
                'birth_date': datetime(1955, 1, 28).date(),
                'education_level': 'NONE',
                'education_years': 0,
                'room_number': '106B',
            },
            {
                'full_name': 'José Pereira',
                'birth_date': datetime(1942, 11, 7).date(),
                'education_level': 'MEDIO',
                'education_years': 11,
                'room_number': '107C',
            },
            {
                'full_name': 'Lucia Rodrigues',
                'birth_date': datetime(1957, 4, 25).date(),
                'education_level': 'GRADUACAO',
                'education_years': 15,
                'room_number': '108A',
            }
        ]
        
        patients = []
        for data in patients_data:
            # usar combinação de nome + data de nascimento para evitar duplicatas
            defaults = {
                'education_level': data['education_level'],
                'education_years': data['education_years'],
                'room_number': data['room_number'],
            }
            patient, created = Patient.objects.get_or_create(
                full_name=data['full_name'],
                birth_date=data['birth_date'],
                defaults=defaults
            )
            if created:
                self.stdout.write(f'Paciente criado: {patient.full_name}')
            patients.append(patient)
        
        return patients

    def create_assessments(self, patients):
        """Cria avaliações de exemplo"""
        evaluators = list(EvaluatorProfile.objects.all())
        
        for i, patient in enumerate(patients):
            # Criar 1-3 avaliações por paciente
            num_assessments = random.randint(1, 3)
            
            for j in range(num_assessments):
                days_ago = random.randint(1, 30)
                created_at = timezone.now() - timedelta(days=days_ago)
                
                assessment = Assessment.objects.create(
                    patient=patient,
                    assessor=random.choice(evaluators).user,
                    status='COMPLETED' if j < num_assessments - 1 else random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
                )
                # ajustar created_at para simular histórico
                assessment.created_at = created_at
                assessment.save(update_fields=['created_at'])
                
                # Criar resultados dos testes se a avaliação estiver completa
                if assessment.status == 'COMPLETED':
                    self.create_test_results(assessment, patient)
                
                self.stdout.write(f'Avaliação criada: {assessment.id} - {patient.full_name}')

    def create_test_results(self, assessment, patient):
        """Cria resultados dos testes"""
        # Digit Span Test
        forward_score = random.randint(4, 12)
        backward_score = random.randint(3, 10)
        
        DigitSpanResult.objects.create(
            assessment=assessment,
            forward_score=forward_score,
            forward_span=random.randint(4, 8),
            backward_score=backward_score,
            backward_span=random.randint(3, 7),
        )
        
        # TMT Test
        age = patient.age
        education_group = 'high_education' if patient.education_level in ['GRADUACAO', 'POSGRAD'] else 'low_education'
        
        # Tempos baseados na idade e escolaridade (com variação)
        base_tmt_a = 30 + (age - 60) * 0.5
        base_tmt_b = 75 + (age - 60) * 1.2
        
        if education_group == 'low_education':
            base_tmt_a *= 1.2
            base_tmt_b *= 1.3
        
        tmt_a_time = max(20, base_tmt_a + random.uniform(-10, 15))
        tmt_b_time = max(45, base_tmt_b + random.uniform(-20, 30))
        
        TMTResult.objects.create(
            assessment=assessment,
            time_a_seconds=round(tmt_a_time, 1),
            errors_a=random.randint(0, 2),
            time_b_seconds=round(tmt_b_time, 1),
            errors_b=random.randint(0, 3)
        )
        
        # Stroop Test
        base_time_1 = 20 + random.uniform(-3, 5)
        base_time_2 = 18 + random.uniform(-3, 5)
        base_time_3 = 35 + (age - 60) * 0.3 + random.uniform(-5, 10)
        
        if education_group == 'low_education':
            base_time_3 *= 1.2
        
        StroopResult.objects.create(
            assessment=assessment,
            card_1_time=round(base_time_1, 1),
            card_1_errors=random.randint(0, 1),
            card_2_time=round(base_time_2, 1),
            card_2_errors=random.randint(0, 1),
            card_3_time=round(base_time_3, 1),
            card_3_errors=random.randint(0, 2)
        )
