#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando deploy do AvivaMente..."

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Executar migrações
echo "🗄️ Executando migrações do banco de dados..."
python manage.py migrate --noinput

# Criar superusuário se não existir
echo "👤 Verificando superusuário..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@caresense.com', 'admin123')
    print('✅ Superusuário criado: admin/admin123')
else:
    print('✅ Superusuário já existe')
"

echo "✅ Deploy concluído com sucesso!"
