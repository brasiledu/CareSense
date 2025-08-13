from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        # Importa os signals para criação de superusuário admin/admin em produção (apenas se não existir)
        try:
            from . import signals  # noqa: F401
        except Exception:
            # Evita quebrar em migrações iniciais
            pass
