from django.contrib import admin
from django.urls import path, include
from apps.core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),  # Página inicial
    path('healthz/', core_views.healthz, name='healthz'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('patients/', core_views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', core_views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/history/', core_views.patient_history, name='patient_history'),
    path('assessments/', core_views.assessment_list, name='assessment_list'),
    path('assessments/<int:assessment_id>/', core_views.assessment_detail, name='assessment_detail'),
    
    # Aplicação de avaliadores
    path('evaluators/', include('evaluators.urls')),
    
    # Funcionalidade principal - Executar testes
    path('start_assessment/', core_views.start_assessment, name='start_assessment'),
    path('assessments/<int:assessment_id>/tests/', core_views.run_tests, name='run_tests'),
    path('assessments/<int:assessment_id>/digit-span/', core_views.run_digit_span, name='run_digit_span'),
    path('assessments/<int:assessment_id>/tmt/', core_views.run_tmt, name='run_tmt'),
    path('assessments/<int:assessment_id>/stroop/', core_views.run_stroop, name='run_stroop'),
    path('assessments/<int:assessment_id>/complete/', core_views.complete_assessment, name='complete_assessment'),
    
    path('admin/', admin.site.urls),
]
