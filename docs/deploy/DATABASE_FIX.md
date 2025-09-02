# 🗄️ Solução para Problemas de Banco de Dados

## Problema
```
psycopg.errors.DuplicateColumn: column "assessor_id" of relation "assessments_assessment" already exists
```

## Causa
O banco PostgreSQL no Render já possui tabelas de deploys anteriores, mas as migrações tentam criar colunas que já existem.

## ✅ Solução Implementada

### Estratégia de Deploy Robusta
O sistema agora usa uma abordagem step-by-step para lidar com migrações:

1. **🔍 Cria migrações necessárias**
2. **📋 Se encontrar tabelas Django:**
   - Usa tabelas existentes
   - Aplica apenas migrações pendentes
   - Ou marca migrações como já aplicadas (`--fake-initial`)
3. **🆕 Se banco estiver vazio:**
   - Cria migrações frescas
   - Aplica todas as migrações

### 🔧 Configuração nos Scripts de Build
```bash
# Em vez de:
python manage.py makemigrations
python manage.py migrate

# Agora usa:
python manage.py makemigrations
python manage.py migrate --fake-initial
```

## 🚨 Solução Manual (se necessário)

### Opção 1: Limpar Banco Completamente
```bash
# No shell do Render ou localmente
python manage.py force_clean_db --confirm
```

### Opção 2: Usar Tabelas Existentes
```bash
# Marcar migrações como já aplicadas
python manage.py migrate --fake-initial

# Aplicar apenas novas migrações
python manage.py migrate
```

### Opção 3: Via Painel Render
1. Vá no PostgreSQL Database
2. Clique em "Shell" 
3. Execute:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

## 🎯 No Render

### Variáveis de Ambiente para Controle
```
FORCE_CLEAN_DB=true  # Para forçar limpeza (usar apenas uma vez)
```

### Build Command Atualizado
```bash
./build.sh
```

O script agora é inteligente e resolve automaticamente!

## 📊 Logs Esperados

### ✅ Sucesso com Tabelas Existentes:
```
🔍 Verificando estado do banco de dados...
📋 Encontradas 25 tabelas Django existentes
✅ Usando banco existente - aplicando apenas novas migrações
```

### ✅ Sucesso com Banco Novo:
```
🔍 Verificando estado do banco de dados...
🆕 Banco vazio - criando estrutura completa
📝 Criando migrações para assessments...
```

## 🛠️ Comandos Úteis

```bash
# Verificar migrações pendentes
python manage.py showmigrations

# Criar migrações necessárias
python manage.py makemigrations

# Aplicar migrações com fallback
python manage.py migrate --fake-initial
python manage.py showmigrations

# Aplicar migrações específicas
python manage.py migrate assessments
```

Esta solução garante que o deploy sempre funcione, seja com banco novo ou existente! 🎉
