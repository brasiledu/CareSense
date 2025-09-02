#!/usr/bin/env bash
# Start script for CareSense Django application

echo "🚀 Starting CareSense server..."

# Verificar se o Django está funcionando
echo "🔍 Checking Django installation..."
python manage.py check

# Verificar conexão com banco
echo "🗄️ Checking database connection..."
python manage.py check --database default

# Iniciar o servidor Gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn caresense_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
