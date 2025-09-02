#!/usr/bin/env python3
"""
Validação pré-deploy para CareSense
Verifica se todos os arquivos e configurações estão corretos antes do deploy.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica se um arquivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (não encontrado)")
        return False

def check_directory_exists(dirpath, description):
    """Verifica se um diretório existe"""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} (não encontrado)")
        return False

def main():
    print("🔍 CareSense - Validação Pré-Deploy")
    print("=" * 50)
    
    base_dir = Path(__file__).parent.parent.parent
    os.chdir(base_dir)
    
    success = True
    
    # Verificar arquivos de deploy
    print("\n📦 Arquivos de Deploy:")
    success &= check_file_exists("deploy/build.sh", "Script de build")
    success &= check_file_exists("deploy/render.yaml", "Configuração Render")
    success &= check_file_exists("deploy/runtime.txt", "Runtime Python")
    
    # Verificar requirements
    print("\n📋 Requirements:")
    success &= check_file_exists("requirements.txt", "Requirements principal")
    success &= check_file_exists("requirements/requirements-prod.txt", "Requirements produção")
    success &= check_file_exists("requirements/requirements-dev.txt", "Requirements desenvolvimento")
    
    # Verificar scripts
    print("\n🔧 Scripts:")
    success &= check_file_exists("scripts/utils/generate_secret_key.py", "Gerador SECRET_KEY")
    
    # Verificar configurações
    print("\n⚙️ Configurações:")
    success &= check_file_exists("config/.env.example", "Exemplo de configuração")
    success &= check_file_exists("caresense_project/settings.py", "Settings Django")
    
    # Verificar documentação
    print("\n📖 Documentação:")
    success &= check_file_exists("docs/deploy/DEPLOY_RENDER.md", "Guia de deploy")
    success &= check_file_exists("README.md", "README principal")
    
    # Verificar estrutura de apps
    print("\n🏗️ Estrutura de Apps:")
    success &= check_directory_exists("apps", "Diretório de apps")
    success &= check_directory_exists("apps/patients", "App patients")
    success &= check_directory_exists("apps/assessments", "App assessments")
    success &= check_directory_exists("apps/users", "App users")
    success &= check_directory_exists("apps/core", "App core")
    
    # Verificar permissões do build script
    print("\n🔐 Permissões:")
    if os.path.exists("deploy/build.sh"):
        if os.access("deploy/build.sh", os.X_OK):
            print("✅ build.sh tem permissão de execução")
        else:
            print("❌ build.sh precisa de permissão de execução")
            print("   Execute: chmod +x deploy/build.sh")
            success = False
    
    # Resultado final
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCESSO: Projeto pronto para deploy!")
        print("\nPróximos passos:")
        print("1. Commite as alterações no Git")
        print("2. Siga o guia: docs/deploy/DEPLOY_RENDER.md")
        print("3. Configure o repositório no Render")
        return 0
    else:
        print("⚠️  ERRO: Corrija os problemas antes do deploy")
        return 1

if __name__ == "__main__":
    sys.exit(main())
