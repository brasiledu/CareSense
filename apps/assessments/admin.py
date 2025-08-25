from django.contrib import admin
from .models import Assessment, DigitSpanResult, TMTResult, StroopResult, MeemResult, ClockDrawingResult

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'assessor', 'status', 'final_risk_score', 'created_at', 'completed_at']
    list_filter = ['status', 'final_risk_score', 'created_at']
    search_fields = ['patient__full_name', 'assessor__username']
    readonly_fields = ['created_at', 'completed_at']
    
    fieldsets = (
        (None, {
            'fields': ('patient', 'assessor', 'status', 'final_risk_score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DigitSpanResult)
class DigitSpanResultAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'forward_score', 'backward_score', 'total_score', 'z_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['assessment__patient__full_name']
    readonly_fields = ['z_score', 'created_at', 'total_score']

@admin.register(TMTResult)
class TMTResultAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'time_a_seconds', 'time_b_seconds', 'errors_a', 'errors_b', 'created_at']
    list_filter = ['created_at']
    search_fields = ['assessment__patient__full_name']
    readonly_fields = ['z_score_a', 'z_score_b', 'created_at']

@admin.register(StroopResult)
class StroopResultAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'card_1_time', 'card_2_time', 'card_3_time', 'interference_time', 'z_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['assessment__patient__full_name']
    readonly_fields = ['z_score', 'created_at', 'interference_time']

@admin.register(MeemResult)
class MeemResultAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'total_score', 'interpretation', 'z_score', 'created_at']
    list_filter = ['interpretation', 'created_at']
    search_fields = ['assessment__patient__full_name']
    readonly_fields = ['total_score', 'interpretation', 'z_score', 'created_at']
    
    fieldsets = (
        ('Informações da Avaliação', {
            'fields': ('assessment',)
        }),
        ('Orientação Temporal (5 pontos)', {
            'fields': ('temporal_weekday', 'temporal_day', 'temporal_month', 'temporal_year', 'temporal_hour'),
            'classes': ('collapse',)
        }),
        ('Orientação Espacial (5 pontos)', {
            'fields': ('spatial_location', 'spatial_place', 'spatial_neighborhood', 'spatial_city', 'spatial_state'),
            'classes': ('collapse',)
        }),
        ('Memória Imediata (3 pontos)', {
            'fields': ('memory_word1', 'memory_word2', 'memory_word3'),
            'classes': ('collapse',)
        }),
        ('Atenção e Cálculo (5 pontos)', {
            'fields': ('attention_calc1', 'attention_calc2', 'attention_calc3', 'attention_calc4', 'attention_calc5'),
            'classes': ('collapse',)
        }),
        ('Evocação (3 pontos)', {
            'fields': ('recall_word1', 'recall_word2', 'recall_word3'),
            'classes': ('collapse',)
        }),
        ('Nomeação (2 pontos)', {
            'fields': ('naming_object1', 'naming_object2'),
            'classes': ('collapse',)
        }),
        ('Repetição (1 ponto)', {
            'fields': ('repetition_phrase',),
            'classes': ('collapse',)
        }),
        ('Comando Verbal (3 pontos)', {
            'fields': ('command_take', 'command_fold', 'command_put'),
            'classes': ('collapse',)
        }),
        ('Comando Escrito (1 ponto)', {
            'fields': ('written_command',),
            'classes': ('collapse',)
        }),
        ('Escrita (1 ponto)', {
            'fields': ('write_sentence',),
            'classes': ('collapse',)
        }),
        ('Habilidade Construtiva (1 ponto)', {
            'fields': ('copy_pentagons',),
            'classes': ('collapse',)
        }),
        ('Resultados', {
            'fields': ('total_score', 'interpretation', 'z_score', 'created_at')
        })
    )

@admin.register(ClockDrawingResult)
class ClockDrawingResultAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'requested_time', 'circle_score', 'numbers_score', 'hands_score', 'total_score', 'classification', 'z_score', 'created_at']
    list_filter = ['classification', 'requested_time', 'created_at']
    search_fields = ['assessment__patient__full_name']
    readonly_fields = ['total_score', 'classification', 'z_score', 'created_at', 'completed_at']
    
    fieldsets = (
        ('Informações da Avaliação', {
            'fields': ('assessment', 'requested_time', 'duration_seconds')
        }),
        ('Pontuação por Componente', {
            'fields': ('circle_score', 'numbers_score', 'hands_score')
        }),
        ('Observações', {
            'fields': ('observations',),
            'classes': ('collapse',)
        }),
        ('Dados do Desenho', {
            'fields': ('drawing_data',),
            'classes': ('collapse',)
        }),
        ('Resultados', {
            'fields': ('total_score', 'classification', 'z_score', 'created_at', 'completed_at')
        })
    )
