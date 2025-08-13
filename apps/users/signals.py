from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import os


@receiver(post_migrate)
def ensure_default_admin(sender, **kwargs):
    """
    Garante um superusuário padrão em ambientes de deploy quando não existir.
    Cria admin/admin por padrão. Pode ser desativado com DISABLE_AUTO_ADMIN=true.
    """
    if os.environ.get('DISABLE_AUTO_ADMIN', 'false').lower() == 'true':
        return

    User = get_user_model()
    # Evita rodar em apps não principais
    if sender.name not in ('auth', 'apps.users'):
        return

    try:
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
            email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@example.com')
            password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin')
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"[INIT] Superusuário criado: {username}/{password}")
    except Exception as e:
        # Apenas loga; não deve quebrar o deploy
        print(f"[INIT] Falha ao garantir superusuário padrão: {e}")
