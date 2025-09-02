# Configuration Files

Esta pasta contém arquivos de configuração para diferentes ambientes.

## Arquivos

### `.env.example`
Exemplo de arquivo de variáveis de ambiente com todas as configurações possíveis:
- Configurações básicas do Django
- Configurações de banco de dados
- Configurações de segurança
- Variáveis para deploy automático

## Uso

### Desenvolvimento Local
1. Copie o arquivo de exemplo:
   ```bash
   cp config/.env.example .env
   ```

2. Edite as variáveis conforme necessário:
   ```bash
   # Gere uma SECRET_KEY
   python scripts/utils/generate_secret_key.py
   
   # Edite o arquivo .env
   nano .env
   ```

3. O Django carregará automaticamente as variáveis do arquivo `.env`

### Produção (Render)
- Use as variáveis de ambiente do painel do Render
- Não commite arquivos `.env` no Git
- Consulte `docs/deploy/DEPLOY_RENDER.md` para instruções completas

## Segurança

⚠️ **IMPORTANTE**:
- Nunca commite arquivos `.env` reais
- Use `.env.example` apenas como template
- Gere novas SECRET_KEY para cada ambiente
- Use senhas fortes em produção
