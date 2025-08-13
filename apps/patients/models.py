from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Patient(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name='Nome Completo'
    )
    
    birth_date = models.DateField(
        verbose_name='Data de Nascimento'
    )
    
    education_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        verbose_name='Anos de Estudo',
        help_text='Número de anos de educação formal'
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
        """Converte anos de estudo em grau de escolaridade"""
        years = self.education_level
        
        if years == 0:
            return "Sem escolaridade"
        elif years <= 4:
            return f"Fundamental I ({years}° ano)"
        elif years <= 8:
            return f"Fundamental II ({years}° ano)"
        elif years == 9:
            return "Fundamental completo"
        elif years <= 11:
            return f"Ensino Médio ({years - 9}° ano)"
        elif years == 12:
            return "Ensino Médio completo"
        elif years <= 16:
            return f"Superior ({years - 12}° ano)"
        elif years >= 17:
            return "Superior completo/Pós-graduação"
        else:
            return f"{years} anos de estudo"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - Quarto {self.room_number}"
    
    @property
    def age(self):
        """Calcula a idade do paciente em anos"""
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))