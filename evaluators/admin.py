from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import EvaluatorProfile


@admin.register(EvaluatorProfile)
class EvaluatorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'crp_number', 'specialization', 'institution', 
        'is_active', 'total_assessments', 'last_login', 'created_at'
    )
    list_filter = ('is_active', 'specialization', 'institution', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'crp_number')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user',)
        }),
        ('Informações Profissionais', {
            'fields': ('crp_number', 'specialization', 'institution', 'phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Datas', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_assessments(self, obj):
        return obj.total_assessments
    total_assessments.short_description = 'Total de Avaliações'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# Customizar o UserAdmin para mostrar apenas avaliadores
class EvaluatorUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_queryset(self, request):
        # Mostrar apenas usuários que são avaliadores (tem perfil de avaliador)
        return super().get_queryset(request).filter(evaluator_profile__isnull=False)


# Reregistrar o User admin apenas se necessário
# admin.site.unregister(User)
# admin.site.register(User, EvaluatorUserAdmin)
