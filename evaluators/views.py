from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from .models import EvaluatorProfile


@never_cache
@csrf_protect
def login_view(request):
    """
    View de login para avaliadores
    """
    print(f"[DEBUG] Login view chamada - Método: {request.method}")
    print(f"[DEBUG] Usuário já autenticado: {request.user.is_authenticated}")
    
    if request.user.is_authenticated:
        print("[DEBUG] Redirecionando usuário autenticado para dashboard")
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"[DEBUG] Tentativa de login - Username: {username}")
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(f"[DEBUG] Autenticação resultado: {user is not None}")
            
            if user is not None:
                if user.is_active:
                    print(f"[DEBUG] Login bem-sucedido para: {user.username}")
                    login(request, user)
                    print(f"[DEBUG] Usuário logado com sucesso: {request.user.is_authenticated}")
                    
                    # Atualizar último login no perfil do avaliador
                    try:
                        profile = user.evaluator_profile
                        profile.update_last_login()
                        print("[DEBUG] Perfil do avaliador atualizado")
                    except EvaluatorProfile.DoesNotExist:
                        # Criar perfil se não existir
                        EvaluatorProfile.objects.create(user=user)
                        profile = user.evaluator_profile
                        profile.update_last_login()
                        print("[DEBUG] Perfil do avaliador criado")
                    
                    messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')
                    
                    # Redirecionar para a página solicitada ou dashboard
                    next_url = request.GET.get('next')
                    if next_url:
                        print(f"[DEBUG] Redirecionando para next_url: {next_url}")
                        return redirect(next_url)
                    else:
                        print("[DEBUG] Redirecionando para dashboard")
                        return redirect('dashboard')
                else:
                    print("[DEBUG] Usuário inativo")
                    messages.error(request, 'Sua conta está desativada. Entre em contato com o administrador.')
            else:
                print("[DEBUG] Credenciais inválidas")
                messages.error(request, 'Credenciais inválidas. Verifique seu usuário e senha.')
        else:
            print("[DEBUG] Campos não preenchidos")
            messages.error(request, 'Por favor, preencha todos os campos.')

    print("[DEBUG] Renderizando template de login")
    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    """
    View de logout para avaliadores
    """
    user_name = request.user.get_full_name() or request.user.username
    logout(request)
    messages.success(request, f'Até logo, {user_name}!')
    return redirect('evaluators:login')


@login_required
def profile_view(request):
    """
    View do perfil do avaliador
    """
    try:
        profile = request.user.evaluator_profile
    except EvaluatorProfile.DoesNotExist:
        # Criar perfil se não existir
        profile = EvaluatorProfile.objects.create(user=request.user)
    
    # Estatísticas do avaliador
    context = {
        'profile': profile,
        'user': request.user,
        'total_assessments': profile.total_assessments,
        'completed_assessments': profile.completed_assessments,
        'pending_assessments': profile.pending_assessments,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def my_assessments_view(request):
    """
    View das avaliações do avaliador logado
    """
    # Importar aqui para evitar import circular
    from apps.assessments.models import Assessment
    
    assessments = Assessment.objects.filter(
        assessor=request.user
    ).select_related('patient').order_by('-created_at')
    
    context = {
        'assessments': assessments,
        'total_count': assessments.count(),
        'pending_count': assessments.filter(status__in=['PENDING', 'IN_PROGRESS']).count(),
        'completed_count': assessments.filter(status='COMPLETED').count(),
    }
    
    return render(request, 'users/my_assessments.html', context)


def check_auth_status(request):
    """
    API endpoint para verificar status de autenticação
    """
    if request.user.is_authenticated:
        try:
            profile = request.user.evaluator_profile
        except EvaluatorProfile.DoesNotExist:
            profile = EvaluatorProfile.objects.create(user=request.user)
        
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
                'last_login': profile.last_login.isoformat() if profile.last_login else None,
            }
        })
    
    return JsonResponse({'authenticated': False})


@login_required
def edit_profile_view(request):
    """
    View para edição do perfil do avaliador
    """
    if request.method == 'POST':
        try:
            # Atualizar dados do usuário
            request.user.first_name = request.POST.get('first_name', '').strip()
            request.user.last_name = request.POST.get('last_name', '').strip()
            request.user.email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            
            # Validar se o username não existe para outro usuário
            if username != request.user.username:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                    messages.error(request, 'Este nome de usuário já está em uso.')
                    return render(request, 'users/edit_profile.html', {'user': request.user})
            
            request.user.username = username
            request.user.save()
            
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('evaluators:profile')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar perfil: {str(e)}')
    
    return render(request, 'users/edit_profile.html', {'user': request.user})


@login_required
def change_password_view(request):
    """
    View para alteração de senha
    """
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Verificar senha atual
        if not request.user.check_password(current_password):
            messages.error(request, 'Senha atual incorreta.')
            return redirect('evaluators:edit_profile')
        
        # Verificar se as novas senhas coincidem
        if new_password1 != new_password2:
            messages.error(request, 'As novas senhas não coincidem.')
            return redirect('evaluators:edit_profile')
        
        # Validar nova senha
        if len(new_password1) < 8:
            messages.error(request, 'A nova senha deve ter pelo menos 8 caracteres.')
            return redirect('evaluators:edit_profile')
        
        try:
            # Alterar senha
            request.user.set_password(new_password1)
            request.user.save()
            
            # Manter o usuário logado após alterar a senha
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('evaluators:profile')
            
        except Exception as e:
            messages.error(request, f'Erro ao alterar senha: {str(e)}')
    
    return redirect('evaluators:edit_profile')
