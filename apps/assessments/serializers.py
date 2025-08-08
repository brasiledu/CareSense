from rest_framework import serializers
from .models import Assessment, DigitSpanResult, TMTResult, StroopResult
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
    patient_education = serializers.IntegerField(source='patient.education_level', read_only=True)
    assessor_name = serializers.CharField(source='assessor.get_full_name', read_only=True)
    digit_span_result = DigitSpanResultSerializer(read_only=True)
    tmt_result = TMTResultSerializer(read_only=True)
    stroop_result = StroopResultSerializer(read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'patient', 'patient_name', 'patient_age', 'patient_education',
            'assessor', 'assessor_name', 'status', 'final_risk_score',
            'created_at', 'completed_at', 'digit_span_result', 'tmt_result', 'stroop_result'
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