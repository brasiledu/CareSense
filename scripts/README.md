# 🔧 Scripts Utilitários do CareSense

Esta pasta contém scripts auxiliares para desenvolvimento, testes e configuração do projeto.

## 📁 Estrutura de Pastas

### 🚀 `/setup/`
Scripts para configuração inicial e deploy do sistema.

#### Arquivos:
- [`create_demo_data.py`](./setup/create_demo_data.py) - Script para criar dados de demonstração
- [`deploy-setup.sh`](./setup/deploy-setup.sh) - Script de configuração para deploy

### 🧪 `/tests/`
Scripts de teste standalone para validação de funcionalidades específicas.

#### Arquivos:
- [`test_meem_implementation.py`](./tests/test_meem_implementation.py) - Testes para o modelo e serializers do MEEM
- [`test_meem_views.py`](./tests/test_meem_views.py) - Testes para as views e endpoints do MEEM

## 🔧 Como Usar os Scripts

### Executar Dados de Demo
```bash
cd caresense-project
python scripts/setup/create_demo_data.py
```

### Executar Testes MEEM
```bash
cd caresense-project
python scripts/tests/test_meem_implementation.py
python scripts/tests/test_meem_views.py
```

### Setup de Deploy
```bash
cd caresense-project
chmod +x scripts/setup/deploy-setup.sh
./scripts/setup/deploy-setup.sh
```

## 📝 Convenções

- Scripts de setup devem ser idempotentes (podem ser executados múltiplas vezes)
- Scripts de teste devem ser independentes e não afetar dados de produção
- Incluir documentação inline nos scripts para explicar funcionalidades complexas
- Usar nomes descritivos para novos scripts

## 🚀 Próximos Scripts Planejados

- Script de backup do banco de dados
- Script de validação de integridade dos dados
- Script de migração de dados entre ambientes
- Testes automatizados para Clock Drawing Test

---
*Última atualização: Agosto 2025*
