#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instalar dependências de produção
pip install -r requirements/requirements-prod.txt

# Coletando arquivos estáticos
python manage.py collectstatic --noinput

# Executar migrações
python manage.py migrate

# Criar superusuário se não existir (apenas em produção)
if [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py create_superuser
fi
