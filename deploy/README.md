# Deploy Configuration

Esta pasta contém os arquivos necessários para fazer deploy da aplicação CareSense.

## Arquivos

### `build.sh`
Script de build executado pelo Render durante o deploy. Responsável por:
- Instalar dependências Python
- Coletar arquivos estáticos
- Executar migrações do banco
- Criar superusuário

### `render.yaml`
Configuração declarativa para deploy no Render. Define:
- Web Service (aplicação Django)
- PostgreSQL Database
- Variáveis de ambiente
- Comandos de build e start

### `runtime.txt`
Especifica a versão do Python a ser usada no deploy (3.12.0).

## Deploy no Render

1. Conecte o repositório GitHub ao Render
2. Use as configurações em `render.yaml` ou configure manualmente
3. O build será executado automaticamente

Para instruções detalhadas, consulte: `docs/deploy/DEPLOY_RENDER.md`
