#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Iniciando build do CareSense..."

# Atualizar pip primeiro
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências de produção
echo "📦 Instalando dependências..."
pip install -r requirements/requirements-prod.txt

# Coletando arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Configurar banco de dados de forma robusta
echo "🗄️ Configurando banco de dados..."

# Verificar se há migrações para fazer
python manage.py makemigrations

# Tentar migração normal
echo "🔄 Aplicando migrações..."
if ! python manage.py migrate; then
    echo "⚠️ Erro na migração normal, tentando com --fake-initial..."
    python manage.py migrate --fake-initial
fi

# Criar superusuário apenas se configurado
if [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Criando superusuário..."
    python manage.py create_superuser
fi

echo "✅ Build concluído com sucesso!"
