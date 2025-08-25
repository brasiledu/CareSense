from rest_framework import serializers
from .models import Assessment, DigitSpanResult, TMTResult, StroopResult, MeemResult, ClockDrawingResult
from apps.patients.models import Patient

class DigitSpanResultSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    
    class Meta:
        model = DigitSpanResult
        fields = [
            'forward_score', 'forward_span', 'backward_score', 
            'backward_span', 'total_score', 'z_score', 'created_at'
        ]
        read_only_fields = ['z_score', 'created_at']

class TMTResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMTResult
        fields = [
            'time_a_seconds', 'errors_a', 'time_b_seconds', 
            'errors_b', 'z_score_a', 'z_score_b', 'created_at'
        ]
        read_only_fields = ['z_score_a', 'z_score_b', 'created_at']

class StroopResultSerializer(serializers.ModelSerializer):
    interference_time = serializers.ReadOnlyField()
    
    class Meta:
        model = StroopResult
        fields = [
            'card_1_time', 'card_1_errors', 'card_2_time', 'card_2_errors',
            'card_3_time', 'card_3_errors', 'interference_time', 'z_score', 'created_at'
        ]
        read_only_fields = ['z_score', 'created_at']

class MeemResultSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    interpretation = serializers.ReadOnlyField()
    z_score = serializers.ReadOnlyField()
    
    class Meta:
        model = MeemResult
        fields = [
            # Orientação Temporal
            'temporal_weekday', 'temporal_day', 'temporal_month', 
            'temporal_year', 'temporal_hour',
            # Orientação Espacial
            'spatial_location', 'spatial_place', 'spatial_neighborhood',
            'spatial_city', 'spatial_state',
            # Memória Imediata
            'memory_word1', 'memory_word2', 'memory_word3',
            # Atenção e Cálculo
            'attention_calc1', 'attention_calc2', 'attention_calc3',
            'attention_calc4', 'attention_calc5',
            # Evocação
            'recall_word1', 'recall_word2', 'recall_word3',
            # Nomeação
            'naming_object1', 'naming_object2',
            # Repetição
            'repetition_phrase',
            # Comando verbal
            'command_take', 'command_fold', 'command_put',
            # Comando escrito
            'written_command',
            # Escrita
            'write_sentence',
            # Habilidade Construtiva
            'copy_pentagons',
            # Campos calculados
            'total_score', 'interpretation', 'z_score', 'created_at'
        ]
        read_only_fields = ['total_score', 'interpretation', 'z_score', 'created_at']

class ClockDrawingResultSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    interpretation = serializers.ReadOnlyField()
    component_scores = serializers.ReadOnlyField()
    detailed_feedback = serializers.ReadOnlyField()
    
    class Meta:
        model = ClockDrawingResult
        fields = [
            'requested_time', 'circle_score', 'numbers_score', 'hands_score',
            'total_score', 'z_score', 'classification', 'observations',
            'drawing_data', 'duration_seconds', 'interpretation',
            'component_scores', 'detailed_feedback', 'created_at', 'completed_at'
        ]
        read_only_fields = [
            'total_score', 'z_score', 'classification', 'interpretation',
            'component_scores', 'detailed_feedback', 'created_at', 'completed_at'
        ]

class AssessmentListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de assessments"""
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_room = serializers.CharField(source='patient.room_number', read_only=True)
    assessor_name = serializers.CharField(source='assessor.get_full_name', read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'patient_name', 'patient_room', 'assessor_name',
            'status', 'final_risk_score', 'created_at', 'completed_at'
        ]

class AssessmentDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalhes completos do assessment"""
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_age = serializers.IntegerField(source='patient.age', read_only=True)
    # Compat: patient_education agora retorna o rótulo do nível
    patient_education = serializers.CharField(source='patient.get_education_level_display', read_only=True)
    # Campos adicionais explícitos
    patient_education_level = serializers.CharField(source='patient.education_level', read_only=True)
    patient_education_years = serializers.IntegerField(source='patient.education_years', read_only=True)
    assessor_name = serializers.CharField(source='assessor.get_full_name', read_only=True)
    digit_span_result = DigitSpanResultSerializer(read_only=True)
    tmt_result = TMTResultSerializer(read_only=True)
    stroop_result = StroopResultSerializer(read_only=True)
    meem_result = MeemResultSerializer(read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'patient', 'patient_name', 'patient_age', 'patient_education',
            'patient_education_level', 'patient_education_years',
            'assessor', 'assessor_name', 'status', 'final_risk_score',
            'created_at', 'completed_at', 'digit_span_result', 'tmt_result', 'stroop_result', 'meem_result'
        ]

class AssessmentCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar um novo assessment"""
    
    class Meta:
        model = Assessment
        fields = ['patient', 'assessor']
    
    def create(self, validated_data):
        validated_data['status'] = 'PENDING'
        return super().create(validated_data)

class SubmitDigitSpanSerializer(serializers.Serializer):
    """Serializer para submeter resultado do Digit Span"""
    forward_score = serializers.IntegerField(min_value=0, max_value=20)
    forward_span = serializers.IntegerField(min_value=0, max_value=10)
    backward_score = serializers.IntegerField(min_value=0, max_value=20)
    backward_span = serializers.IntegerField(min_value=0, max_value=10)
    
    def validate(self, data):
        """Validações customizadas"""
        if data['forward_span'] > data['forward_score']:
            raise serializers.ValidationError("Forward span não pode ser maior que forward score")
        if data['backward_span'] > data['backward_score']:
            raise serializers.ValidationError("Backward span não pode ser maior que backward score")
        return data

class SubmitTMTSerializer(serializers.Serializer):
    """Serializer para submeter resultado do TMT"""
    time_a_seconds = serializers.FloatField(min_value=0)
    errors_a = serializers.IntegerField(min_value=0, default=0)
    time_b_seconds = serializers.FloatField(min_value=0)
    errors_b = serializers.IntegerField(min_value=0, default=0)

class SubmitStroopSerializer(serializers.Serializer):
    """Serializer para submeter resultado do Stroop"""
    card_1_time = serializers.FloatField(min_value=0)
    card_1_errors = serializers.IntegerField(min_value=0, default=0)
    card_2_time = serializers.FloatField(min_value=0)
    card_2_errors = serializers.IntegerField(min_value=0, default=0)
    card_3_time = serializers.FloatField(min_value=0)
    card_3_errors = serializers.IntegerField(min_value=0, default=0)

class SubmitMeemSerializer(serializers.Serializer):
    """Serializer para submeter resultado do MEEM"""
    # Orientação Temporal (5 pontos)
    temporal_weekday = serializers.IntegerField(min_value=0, max_value=1)
    temporal_day = serializers.IntegerField(min_value=0, max_value=1)
    temporal_month = serializers.IntegerField(min_value=0, max_value=1)
    temporal_year = serializers.IntegerField(min_value=0, max_value=1)
    temporal_hour = serializers.IntegerField(min_value=0, max_value=1)
    
    # Orientação Espacial (5 pontos)
    spatial_location = serializers.IntegerField(min_value=0, max_value=1)
    spatial_place = serializers.IntegerField(min_value=0, max_value=1)
    spatial_neighborhood = serializers.IntegerField(min_value=0, max_value=1)
    spatial_city = serializers.IntegerField(min_value=0, max_value=1)
    spatial_state = serializers.IntegerField(min_value=0, max_value=1)
    
    # Memória Imediata (3 pontos)
    memory_word1 = serializers.IntegerField(min_value=0, max_value=1)
    memory_word2 = serializers.IntegerField(min_value=0, max_value=1)
    memory_word3 = serializers.IntegerField(min_value=0, max_value=1)
    
    # Atenção e Cálculo (5 pontos)
    attention_calc1 = serializers.IntegerField(min_value=0, max_value=1)
    attention_calc2 = serializers.IntegerField(min_value=0, max_value=1)
    attention_calc3 = serializers.IntegerField(min_value=0, max_value=1)
    attention_calc4 = serializers.IntegerField(min_value=0, max_value=1)
    attention_calc5 = serializers.IntegerField(min_value=0, max_value=1)
    
    # Evocação (3 pontos)
    recall_word1 = serializers.IntegerField(min_value=0, max_value=1)
    recall_word2 = serializers.IntegerField(min_value=0, max_value=1)
    recall_word3 = serializers.IntegerField(min_value=0, max_value=1)
    
    # Nomeação (2 pontos)
    naming_object1 = serializers.IntegerField(min_value=0, max_value=1)
    naming_object2 = serializers.IntegerField(min_value=0, max_value=1)
    
    # Repetição (1 ponto)
    repetition_phrase = serializers.IntegerField(min_value=0, max_value=1)
    
    # Comando verbal (3 pontos)
    command_take = serializers.IntegerField(min_value=0, max_value=1)
    command_fold = serializers.IntegerField(min_value=0, max_value=1)
    command_put = serializers.IntegerField(min_value=0, max_value=1)
    
    # Comando escrito (1 ponto)
    written_command = serializers.IntegerField(min_value=0, max_value=1)
    
    # Escrita (1 ponto)
    write_sentence = serializers.IntegerField(min_value=0, max_value=1)
    
    # Habilidade Construtiva (1 ponto)
    copy_pentagons = serializers.IntegerField(min_value=0, max_value=1)
    
    def validate(self, data):
        """Validações customizadas"""
        # Calcular total para verificar se está dentro do esperado
        total = sum(data.values())
        if total > 30:
            raise serializers.ValidationError("A pontuação total não pode exceder 30 pontos")
        return data

class SubmitClockDrawingSerializer(serializers.Serializer):
    """Serializer para submissão do Clock Drawing Test via API"""
    
    requested_time = serializers.CharField(max_length=10)
    circle_score = serializers.IntegerField(min_value=0, max_value=2)
    numbers_score = serializers.IntegerField(min_value=0, max_value=4)
    hands_score = serializers.IntegerField(min_value=0, max_value=4)
    observations = serializers.CharField(required=False, allow_blank=True)
    drawing_data = serializers.CharField(required=False, allow_blank=True)
    duration_seconds = serializers.IntegerField(min_value=0, required=False)
    
    def validate_requested_time(self, value):
        """Validar formato da hora"""
        valid_times = ['10:05', '11:10', '14:30', '15:45', '20:20']
        if value not in valid_times:
            raise serializers.ValidationError(f"Hora deve ser uma das opções: {', '.join(valid_times)}")
        return value
    
    def validate(self, data):
        """Validações customizadas"""
        total = data['circle_score'] + data['numbers_score'] + data['hands_score']
        if total > 10:
            raise serializers.ValidationError("A pontuação total não pode exceder 10 pontos")
        return data