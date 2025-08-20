from rest_framework import serializers
from .models import Patient, EducationLevel

class PatientSerializer(serializers.ModelSerializer):
    education_label = serializers.CharField(source='get_education_level_display', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'birth_date', 'education_level', 'education_label', 'education_years', 'room_number', 'created_at', 'updated_at']

    def validate_education_level(self, value):
        # Aceita tanto o choice (str) quanto anos (int/str numérica)
        if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
            years = int(value)
            if years == 0:
                return EducationLevel.NONE
            elif years <= 8:
                return EducationLevel.FUNDAMENTAL
            elif years <= 11:
                return EducationLevel.MEDIO
            elif years <= 16:
                return EducationLevel.GRADUACAO
            else:
                return EducationLevel.POSGRAD
        # Valida se está entre os choices
        valid_values = {choice[0] for choice in EducationLevel.choices}
        if value not in valid_values:
            raise serializers.ValidationError('Escolaridade inválida. Use um dos níveis definidos ou informe anos (número).')
        return value