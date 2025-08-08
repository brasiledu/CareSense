from django.db import models
from django.conf import settings
from django.utils import timezone

class Assessment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('IN_PROGRESS', 'Em Andamento'),
        ('COMPLETED', 'Concluído'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    RISK_SCORE_CHOICES = [
        ('LOW', 'Baixo'),
        ('MODERATE', 'Moderado'),
        ('HIGH', 'Alto'),
        ('CRITICAL', 'Crítico'),
    ]
    
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='assessments',
        verbose_name='Paciente'
    )
    
    assessor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assessments',
        verbose_name='Avaliador'
    )
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Status'
    )
    
    final_risk_score = models.CharField(
        max_length=10,
        choices=RISK_SCORE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Pontuação Final de Risco'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Avaliação {self.id} - {self.patient.full_name}"
    
    def mark_completed(self):
        """Marca a avaliação como concluída"""
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save()

class DigitSpanResult(models.Model):
    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        related_name='digit_span_result',
        verbose_name='Avaliação'
    )
    
    forward_score = models.IntegerField(
        verbose_name='Pontuação Direta'
    )
    
    forward_span = models.IntegerField(
        verbose_name='Span Direto'
    )
    
    backward_score = models.IntegerField(
        verbose_name='Pontuação Inversa'
    )
    
    backward_span = models.IntegerField(
        verbose_name='Span Inverso'
    )
    
    z_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Z-Score'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Resultado Span de Dígitos'
        verbose_name_plural = 'Resultados Span de Dígitos'
    
    def __str__(self):
        return f"Digit Span - {self.assessment.patient.full_name}"
    
    @property
    def total_score(self):
        """Retorna a pontuação total (forward + backward)"""
        return self.forward_score + self.backward_score

class TMTResult(models.Model):
    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        related_name='tmt_result',
        verbose_name='Avaliação'
    )
    
    time_a_seconds = models.FloatField(
        verbose_name='Tempo TMT-A (segundos)'
    )
    
    errors_a = models.IntegerField(
        default=0,
        verbose_name='Erros TMT-A'
    )
    
    time_b_seconds = models.FloatField(
        verbose_name='Tempo TMT-B (segundos)'
    )
    
    errors_b = models.IntegerField(
        default=0,
        verbose_name='Erros TMT-B'
    )
    
    z_score_a = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Z-Score TMT-A'
    )
    
    z_score_b = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Z-Score TMT-B'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Resultado TMT'
        verbose_name_plural = 'Resultados TMT'
    
    def __str__(self):
        return f"TMT - {self.assessment.patient.full_name}"

class StroopResult(models.Model):
    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        related_name='stroop_result',
        verbose_name='Avaliação'
    )
    
    card_1_time = models.FloatField(
        verbose_name='Tempo Cartão 1 (segundos)'
    )
    
    card_1_errors = models.IntegerField(
        default=0,
        verbose_name='Erros Cartão 1'
    )
    
    card_2_time = models.FloatField(
        verbose_name='Tempo Cartão 2 (segundos)'
    )
    
    card_2_errors = models.IntegerField(
        default=0,
        verbose_name='Erros Cartão 2'
    )
    
    card_3_time = models.FloatField(
        verbose_name='Tempo Cartão 3 (segundos)'
    )
    
    card_3_errors = models.IntegerField(
        default=0,
        verbose_name='Erros Cartão 3'
    )
    
    z_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Z-Score'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Resultado Stroop'
        verbose_name_plural = 'Resultados Stroop'
    
    def __str__(self):
        return f"Stroop - {self.assessment.patient.full_name}"
    
    @property
    def interference_time(self):
        """Retorna o tempo de interferência (Cartão 3)"""
        return self.card_3_time