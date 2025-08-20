from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class EducationLevel(models.TextChoices):
    NONE = 'NONE', 'Sem escolaridade'
    FUNDAMENTAL = 'FUNDAMENTAL', 'Fundamental'
    MEDIO = 'MEDIO', 'Ensino Médio'
    GRADUACAO = 'GRADUACAO', 'Graduação'
    POSGRAD = 'POSGRAD', 'Pós-graduação'

class Patient(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name='Nome Completo'
    )
    
    birth_date = models.DateField(
        verbose_name='Data de Nascimento'
    )

    # Novo: Escolaridade por nível (choices)
    education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        default=EducationLevel.FUNDAMENTAL,
        verbose_name='Escolaridade',
        help_text='Nível de escolaridade (ex.: Fundamental, Médio, Graduação)'
    )

    # Opcional/Legado: anos de estudo (mantido para referência e migração de dados)
    education_years = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        verbose_name='Anos de Estudo (legado)',
        help_text='Campo legado, opcional. Não é mais utilizado para cálculos.'
    )
    
    room_number = models.CharField(
        max_length=20,
        verbose_name='Número do Quarto'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name
    
    @property
    def age(self):
        """Calcula a idade do paciente"""
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def education_grade(self):
        """Retorna o rótulo amigável da escolaridade"""
        return self.get_education_level_display()