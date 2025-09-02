#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Iniciando build do CareSense..."

# Instalar dependências de produção
echo "📦 Instalando dependências..."
pip install -r requirements-render.txt

# Coletando arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate

# Criar superusuário apenas se configurado
if [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Criando superusuário..."
    python manage.py create_superuser
fi

echo "✅ Build concluído com sucesso!"
