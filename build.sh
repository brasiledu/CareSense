#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Iniciando build do CareSense..."

# Atualizar pip primeiro
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências de produção
echo "📦 Instalando dependências..."
pip install -r requirements-render.txt

# Coletando arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Gerar migrações iniciais (banco limpo)
echo "🔄 Gerando migrações iniciais..."
python manage.py makemigrations

# Executar migrações (criação completa do banco)
echo "🗄️ Criando estrutura do banco..."
python manage.py migrate

# Criar superusuário apenas se configurado
if [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Criando superusuário..."
    python manage.py create_superuser
fi

echo "✅ Build concluído com sucesso!"
