from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'age', 'education_level', 'room_number', 'created_at']
    list_filter = ['education_level', 'created_at']
    search_fields = ['full_name', 'room_number']
    readonly_fields = ['age', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informações do Paciente', {
            'fields': ('full_name', 'birth_date', 'age', 'education_level', 'education_years', 'room_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
