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

class MeemResult(models.Model):
    """
    Resultado do Mini Exame do Estado Mental (MEEM)
    Baseado no protocolo de Folstein & Folstein (1975)
    """
    
    # Relacionamento
    assessment = models.OneToOneField(
        Assessment, 
        on_delete=models.CASCADE,
        related_name='meem_result',
        verbose_name='Avaliação'
    )
    
    # 1. ORIENTAÇÃO TEMPORAL (5 pontos)
    temporal_weekday = models.IntegerField(
        default=0, 
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Dia da semana'
    )
    temporal_day = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')], 
        verbose_name='Data do mês'
    )
    temporal_month = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Mês'
    )
    temporal_year = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Ano'
    )
    temporal_hour = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Hora (±60 min)'
    )
    
    # 2. ORIENTAÇÃO ESPACIAL (5 pontos)
    spatial_location = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Local (consultório/quarto)'
    )
    spatial_place = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Lugar (hospital/clínica)'
    )
    spatial_neighborhood = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Bairro/rua'
    )
    spatial_city = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Cidade'
    )
    spatial_state = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Estado'
    )
    
    # 3. MEMÓRIA IMEDIATA (3 pontos)
    # Palavras sugeridas: carro, vaso, tijolo
    memory_word1 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Palavra 1 (carro)'
    )
    memory_word2 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Palavra 2 (vaso)'
    )
    memory_word3 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Palavra 3 (tijolo)'
    )
    
    # 4. ATENÇÃO E CÁLCULO (5 pontos)
    # Subtrações seriadas de 7: 100-7=93, 93-7=86, 86-7=79, 79-7=72, 72-7=65
    attention_calc1 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='100 - 7 = 93'
    )
    attention_calc2 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='93 - 7 = 86'
    )
    attention_calc3 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='86 - 7 = 79'
    )
    attention_calc4 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='79 - 7 = 72'
    )
    attention_calc5 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='72 - 7 = 65'
    )
    
    # 5. MEMÓRIA DE EVOCAÇÃO (3 pontos)
    recall_word1 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Evocação palavra 1'
    )
    recall_word2 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Evocação palavra 2'
    )
    recall_word3 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Evocação palavra 3'
    )
    
    # 6. NOMEAÇÃO (2 pontos)
    naming_object1 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Nomear relógio'
    )
    naming_object2 = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Nomear caneta'
    )
    
    # 7. REPETIÇÃO (1 ponto)
    repetition_phrase = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Repetir: "Nem aqui, nem ali, nem lá"'
    )
    
    # 8. COMANDO VERBAL (3 pontos)
    command_take = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Pegar folha com mão direita'
    )
    command_fold = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Dobrar ao meio'
    )
    command_put = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Colocar no chão'
    )
    
    # 9. COMANDO ESCRITO (1 ponto)
    written_command = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Ler e executar: "FECHE OS OLHOS"'
    )
    
    # 10. ESCREVER FRASE (1 ponto)
    write_sentence = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Escrever frase (com verbo e sentido)'
    )
    
    # 11. COPIAR DESENHO (1 ponto)
    copy_pentagons = models.IntegerField(
        default=0,
        choices=[(0, 'Incorreto'), (1, 'Correto')],
        verbose_name='Copiar pentágonos intersectados'
    )
    
    # Campos calculados
    total_score = models.IntegerField(
        default=0,
        verbose_name='Pontuação Total (0-30)'
    )
    
    # Interpretação baseada na escolaridade (Brucki et al. 2003)
    INTERPRETATION_CHOICES = [
        ('NORMAL', 'Normal'),
        ('MILD_IMPAIRMENT', 'Comprometimento Leve'),
        ('MODERATE_IMPAIRMENT', 'Comprometimento Moderado'),
        ('SEVERE_IMPAIRMENT', 'Comprometimento Grave'),
        ('REQUIRES_EVALUATION', 'Requer Avaliação Adicional'),
    ]
    
    interpretation = models.CharField(
        max_length=25,
        choices=INTERPRETATION_CHOICES,
        blank=True,
        verbose_name='Interpretação'
    )
    
    # Z-Score para comparação com outros testes
    z_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Z-Score'
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Resultado MEEM"
        verbose_name_plural = "Resultados MEEM"
        
    def __str__(self):
        return f"MEEM - {self.assessment.patient.full_name} - {self.total_score}/30"
    
    def save(self, *args, **kwargs):
        """Calcula automaticamente a pontuação total e interpretação"""
        self.calculate_total_score()
        self.interpret_score()
        super().save(*args, **kwargs)
    
    def calculate_total_score(self):
        """Calcula a pontuação total do MEEM (0-30 pontos)"""
        # Orientação temporal (5 pontos)
        temporal_score = (
            self.temporal_weekday + self.temporal_day + self.temporal_month + 
            self.temporal_year + self.temporal_hour
        )
        
        # Orientação espacial (5 pontos)
        spatial_score = (
            self.spatial_location + self.spatial_place + self.spatial_neighborhood +
            self.spatial_city + self.spatial_state
        )
        
        # Memória imediata (3 pontos)
        memory_score = self.memory_word1 + self.memory_word2 + self.memory_word3
        
        # Atenção e cálculo (5 pontos)
        attention_score = (
            self.attention_calc1 + self.attention_calc2 + self.attention_calc3 +
            self.attention_calc4 + self.attention_calc5
        )
        
        # Evocação (3 pontos)
        recall_score = self.recall_word1 + self.recall_word2 + self.recall_word3
        
        # Nomeação (2 pontos)
        naming_score = self.naming_object1 + self.naming_object2
        
        # Linguagem e comandos (6 pontos)
        language_score = (
            self.repetition_phrase + self.command_take + self.command_fold +
            self.command_put + self.written_command + self.write_sentence
        )
        
        # Habilidade construtiva (1 ponto)
        constructive_score = self.copy_pentagons
        
        # Total
        self.total_score = (
            temporal_score + spatial_score + memory_score + attention_score +
            recall_score + naming_score + language_score + constructive_score
        )
    
    def interpret_score(self):
        """
        Interpreta o score baseado na escolaridade do paciente
        Usando critérios de Brucki et al. (2003)
        """
        patient = self.assessment.patient
        education_years = getattr(patient, 'education_years', 0) or 0
        
        # Pontos de corte baseados em Brucki et al. (2003)
        if education_years == 0:  # Analfabetos
            cutoff = 20
        elif 1 <= education_years <= 4:  # 1-4 anos
            cutoff = 25
        elif 5 <= education_years <= 8:  # 5-8 anos
            cutoff = 26
        elif 9 <= education_years <= 11:  # 9-11 anos
            cutoff = 28
        else:  # >11 anos
            cutoff = 29
        
        # Interpretação
        if self.total_score >= cutoff:
            self.interpretation = 'NORMAL'
        elif self.total_score >= (cutoff - 3):
            self.interpretation = 'MILD_IMPAIRMENT'
        elif self.total_score >= (cutoff - 6):
            self.interpretation = 'MODERATE_IMPAIRMENT'
        elif self.total_score >= (cutoff - 10):
            self.interpretation = 'SEVERE_IMPAIRMENT'
        else:
            self.interpretation = 'REQUIRES_EVALUATION'
    
    def get_domain_scores(self):
        """Retorna pontuações por domínio cognitivo"""
        return {
            'orientacao_temporal': (
                self.temporal_weekday + self.temporal_day + self.temporal_month +
                self.temporal_year + self.temporal_hour
            ),
            'orientacao_espacial': (
                self.spatial_location + self.spatial_place + self.spatial_neighborhood +
                self.spatial_city + self.spatial_state
            ),
            'memoria_imediata': self.memory_word1 + self.memory_word2 + self.memory_word3,
            'atencao_calculo': (
                self.attention_calc1 + self.attention_calc2 + self.attention_calc3 +
                self.attention_calc4 + self.attention_calc5
            ),
            'evocacao': self.recall_word1 + self.recall_word2 + self.recall_word3,
            'nomeacao': self.naming_object1 + self.naming_object2,
            'linguagem': (
                self.repetition_phrase + self.command_take + self.command_fold +
                self.command_put + self.written_command + self.write_sentence
            ),
            'habilidade_construtiva': self.copy_pentagons
        }
    
    def get_cutoff_for_patient(self):
        """Retorna o ponto de corte específico para o paciente"""
        patient = self.assessment.patient
        education_years = getattr(patient, 'education_years', 0) or 0
        
        if education_years == 0:
            return 20, "Analfabeto"
        elif 1 <= education_years <= 4:
            return 25, "1-4 anos de escolaridade"
        elif 5 <= education_years <= 8:
            return 26, "5-8 anos de escolaridade"
        elif 9 <= education_years <= 11:
            return 28, "9-11 anos de escolaridade"
        else:
            return 29, ">11 anos de escolaridade"

class ClockDrawingResult(models.Model):
    """
    Resultado do Teste do Relógio (Clock Drawing Test)
    Baseado no protocolo de Cacho-Gutiérrez et al. (1999)
    """
    
    # Relacionamento
    assessment = models.OneToOneField(
        Assessment, 
        on_delete=models.CASCADE,
        related_name='clock_drawing_result',
        verbose_name='Avaliação'
    )
    
    # Hora solicitada para o teste
    requested_time = models.CharField(
        max_length=10,
        default="10:05",
        verbose_name='Hora Solicitada',
        help_text='Formato HH:MM (ex: 10:05, 11:10)'
    )
    
    # COMPONENTES DE PONTUAÇÃO
    
    # 1. CÍRCULO (0-2 pontos)
    circle_score = models.IntegerField(
        default=0,
        choices=[
            (0, 'Ausente ou gravemente distorcido'),
            (1, 'Presente mas ligeiramente distorcido'),
            (2, 'Círculo perfeito ou quase perfeito')
        ],
        verbose_name='Pontuação do Círculo'
    )
    
    # 2. NÚMEROS (0-4 pontos)
    numbers_score = models.IntegerField(
        default=0,
        choices=[
            (0, 'Números ausentes ou completamente incorretos'),
            (1, 'Alguns números presentes mas com muitos erros'),
            (2, 'Números presentes mas com alguns erros de posição/sequência'),
            (3, 'Todos os números presentes com pequenos erros'),
            (4, 'Todos os 12 números corretos e bem posicionados')
        ],
        verbose_name='Pontuação dos Números'
    )
    
    # 3. PONTEIROS (0-4 pontos)
    hands_score = models.IntegerField(
        default=0,
        choices=[
            (0, 'Ponteiros ausentes ou completamente incorretos'),
            (1, 'Apenas um ponteiro presente ou ambos incorretos'),
            (2, 'Ambos ponteiros presentes mas com hora incorreta'),
            (3, 'Ponteiros presentes, hora quase correta'),
            (4, 'Ambos ponteiros corretos indicando a hora exata')
        ],
        verbose_name='Pontuação dos Ponteiros'
    )
    
    # PONTUAÇÃO TOTAL (0-10)
    total_score = models.IntegerField(
        default=0,
        verbose_name='Pontuação Total'
    )
    
    # Z-Score para padronização
    z_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Z-Score'
    )
    
    # Classificação baseada no ponto de corte (≤6 = deterioração)
    CLASSIFICATION_CHOICES = [
        ('NORMAL', 'Normal (>6 pontos)'),
        ('IMPAIRED', 'Comprometimento Cognitivo (≤6 pontos)')
    ]
    
    classification = models.CharField(
        max_length=10,
        choices=CLASSIFICATION_CHOICES,
        blank=True,
        verbose_name='Classificação'
    )
    
    # Observações do avaliador
    observations = models.TextField(
        blank=True,
        verbose_name='Observações do Avaliador',
        help_text='Detalhes sobre o processo de execução, dificuldades observadas, etc.'
    )
    
    # Dados do desenho (armazenado como base64)
    drawing_data = models.TextField(
        blank=True,
        verbose_name='Dados do Desenho',
        help_text='Imagem do desenho em formato base64'
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)
    duration_seconds = models.IntegerField(
        default=0,
        verbose_name='Duração (segundos)'
    )
    
    class Meta:
        verbose_name = 'Resultado do Teste do Relógio'
        verbose_name_plural = 'Resultados do Teste do Relógio'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Clock Drawing - {self.assessment.patient.full_name} ({self.total_score}/10)"
    
    def save(self, *args, **kwargs):
        # Calcular pontuação total automaticamente
        self.total_score = self.circle_score + self.numbers_score + self.hands_score
        
        # Determinar classificação baseada no ponto de corte
        if self.total_score > 6:
            self.classification = 'NORMAL'
        else:
            self.classification = 'IMPAIRED'
        
        super().save(*args, **kwargs)
    
    def get_component_scores(self):
        """Retorna dicionário com pontuações por componente"""
        return {
            'circulo': self.circle_score,
            'numeros': self.numbers_score,
            'ponteiros': self.hands_score,
            'total': self.total_score
        }
    
    def get_interpretation(self):
        """Retorna interpretação baseada na pontuação"""
        if self.total_score > 6:
            return {
                'status': 'Normal',
                'description': 'Sem indicativos de comprometimento cognitivo',
                'color': '#28a745',
                'icon': 'fas fa-check-circle'
            }
        else:
            return {
                'status': 'Comprometimento Cognitivo',
                'description': 'Pontuação sugere possível deterioração cognitiva',
                'color': '#dc3545',
                'icon': 'fas fa-exclamation-triangle'
            }
    
    def get_detailed_feedback(self):
        """Retorna feedback detalhado por componente"""
        feedback = []
        
        # Análise do círculo
        if self.circle_score == 2:
            feedback.append("✓ Círculo bem desenhado")
        elif self.circle_score == 1:
            feedback.append("△ Círculo presente mas com distorções")
        else:
            feedback.append("✗ Círculo ausente ou muito distorcido")
        
        # Análise dos números
        if self.numbers_score == 4:
            feedback.append("✓ Todos os números corretos e bem posicionados")
        elif self.numbers_score >= 2:
            feedback.append("△ Números presentes mas com alguns erros")
        else:
            feedback.append("✗ Problemas significativos com os números")
        
        # Análise dos ponteiros
        if self.hands_score == 4:
            feedback.append("✓ Ponteiros corretos indicando a hora exata")
        elif self.hands_score >= 2:
            feedback.append("△ Ponteiros presentes mas com imprecisões")
        else:
            feedback.append("✗ Problemas significativos com os ponteiros")
        
        return feedback