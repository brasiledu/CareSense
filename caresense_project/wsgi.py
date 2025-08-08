import os
import sys

from django.core.wsgi import get_wsgi_application

# Define o caminho do projeto
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caresense_project.settings')

# Obtém a aplicação WSGI
application = get_wsgi_application()