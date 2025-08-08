from django.contrib import admin
from .models import Assessment, DigitSpanResult, TMTResult, StroopResult

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
