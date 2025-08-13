from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class EvaluatorProfile(models.Model):
    """
    Perfil extendido para avaliadores
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluator_profile')
    crp_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número do CRP")
    specialization = models.CharField(max_length=100, blank=True, null=True, verbose_name="Especialização")
    institution = models.CharField(max_length=200, blank=True, null=True, verbose_name="Instituição")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Último login")
    
    class Meta:
        verbose_name = "Perfil do Avaliador"
        verbose_name_plural = "Perfis dos Avaliadores"
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.crp_number if self.crp_number else 'Sem CRP'}"
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def total_assessments(self):
        """Retorna o total de avaliações do avaliador"""
        return self.user.assessments.count()
    
    @property
    def completed_assessments(self):
        """Retorna o total de avaliações concluídas"""
        return self.user.assessments.filter(status='COMPLETED').count()
    
    @property
    def pending_assessments(self):
        """Retorna o total de avaliações pendentes"""
        return self.user.assessments.filter(status__in=['PENDING', 'IN_PROGRESS']).count()
    
    def update_last_login(self):
        """Atualiza o último login"""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def save(self, *args, **kwargs):
        # Criar o perfil automaticamente se não existir
        super().save(*args, **kwargs)
