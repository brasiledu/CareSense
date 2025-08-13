from django.urls import path
from . import views

app_name = 'evaluators'

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfil do avaliador
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    
    # Minhas avaliações
    path('my-assessments/', views.my_assessments_view, name='my_assessments'),
    
    # API endpoints
    path('api/auth-status/', views.check_auth_status, name='auth_status'),
]
