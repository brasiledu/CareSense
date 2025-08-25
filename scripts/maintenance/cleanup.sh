#!/bin/bash
# filepath: scripts/maintenance/cleanup.sh
# Script de limpeza e manutenção do projeto CareSense

echo "🧹 Iniciando limpeza do projeto CareSense..."

# Navegar para a raiz do projeto
cd "$(dirname "$0")/../.."

echo "📁 Limpando arquivos cache Python..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -type f -delete 2>/dev/null || true
find . -name "*.pyo" -type f -delete 2>/dev/null || true

echo "🗑️  Removendo arquivos temporários..."
find . -name "*.tmp" -type f -delete 2>/dev/null || true
find . -name "*.temp" -type f -delete 2>/dev/null || true
find . -name "*.swp" -type f -delete 2>/dev/null || true
find . -name "*.swo" -type f -delete 2>/dev/null || true
find . -name "*~" -type f -delete 2>/dev/null || true

echo "🍎 Removendo arquivos do macOS..."
find . -name ".DS_Store" -type f -delete 2>/dev/null || true
find . -name ".DS_Store?" -type f -delete 2>/dev/null || true
find . -name "._*" -type f -delete 2>/dev/null || true

echo "📦 Limpando staticfiles coletados..."
if [ -d "staticfiles" ]; then
    rm -rf staticfiles/*
    echo "Staticfiles limpos"
fi

echo "🧪 Verificando arquivos de teste vazios..."
empty_files=$(find . -name "test_*.py" -size 0 2>/dev/null)
if [ ! -z "$empty_files" ]; then
    echo "⚠️  Arquivos de teste vazios encontrados:"
    echo "$empty_files"
    echo "Execute: rm $empty_files"
fi

echo "📊 Estatísticas do projeto:"
echo "📄 Total de arquivos Python: $(find . -name "*.py" | wc -l)"
echo "📁 Total de templates: $(find templates/ -name "*.html" 2>/dev/null | wc -l || echo 0)"
echo "🧪 Total de testes: $(find . -path "./tests/*" -name "*.py" 2>/dev/null | wc -l || echo 0)"

echo "✅ Limpeza concluída!"
echo ""
echo "🔧 Para executar novamente:"
echo "chmod +x scripts/maintenance/cleanup.sh"
echo "./scripts/maintenance/cleanup.sh"
