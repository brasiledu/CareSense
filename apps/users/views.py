from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

@csrf_protect
def login_view(request):
    """Encaminha para o login de avaliadores, preservando ?next= quando presente."""
    next_url = request.GET.get('next') or request.POST.get('next')
    evaluator_login_url = reverse('evaluators:login')
    if next_url:
        return redirect(f"{evaluator_login_url}?next={next_url}")
    return redirect(evaluator_login_url)

@login_required
def logout_view(request):
    """Logout e redireciona para o login de avaliadores."""
    user_name = request.user.get_full_name()
    logout(request)
    messages.success(request, f'Até logo, {user_name}!')
    return redirect('evaluators:login')

@login_required
def profile_view(request):
    """View para visualizar o perfil do usuário"""
    return render(request, 'users/profile.html', {
        'user': request.user
    })

# API Views (mantidas para compatibilidade)
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)