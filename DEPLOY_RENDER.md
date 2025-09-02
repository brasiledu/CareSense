# Deploy no Render - CareSense

## 📋 Pré-requisitos PRONTOS ✅

- Conta no [Render](https://render.com)
- Repositório: https://github.com/brasiledu/CareSense.git
- **SECRET_KEY gerada:** `+6#zs04%$_a*@u#*k)r0e2_3v)ni_52#jn+-+#l2m+v0o04k+i`

## 🚀 Passo a Passo para Deploy

### 1. Conectar Repositório no Render

1. Acesse [Render Dashboard](https://dashboard.render.com/)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte sua conta do GitHub
4. Selecione o repositório: `brasiledu/CareSense`
5. Clique em **"Connect"**

### 2. Configurar Web Service

**Configurações Básicas:**
- **Name:** `caresense`
- **Region:** `Oregon (US West)`
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn caresense_project.wsgi:application`

### 3. Configurar Variáveis de Ambiente

Na seção **Environment Variables**, adicione:

#### ⚡ Obrigatórias:
```
DEBUG = false
SECRET_KEY = +6#zs04%$_a*@u#*k)r0e2_3v)ni_52#jn+-+#l2m+v0o04k+i
PYTHON_VERSION = 3.12.0
```

#### 🔒 Segurança HTTPS:
```
SECURE_SSL_REDIRECT = true
SESSION_COOKIE_SECURE = true
CSRF_COOKIE_SECURE = true
```

#### 👤 Superusuário (será criado automaticamente):
```
DJANGO_SUPERUSER_USERNAME = admin
DJANGO_SUPERUSER_EMAIL = admin@caresense.com
DJANGO_SUPERUSER_PASSWORD = [DEFINA_UMA_SENHA_FORTE]
```

### 4. Criar Banco PostgreSQL

1. No Dashboard do Render, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `caresense-db`
   - **Database Name:** `caresense`
   - **User:** `caresense`
   - **Region:** `Oregon (US West)` (mesma do web service)
   - **Plan:** `Free`

3. Após criado, vá na aba **"Info"** do PostgreSQL
4. Copie a **"Internal Database URL"**
5. Volte ao Web Service, vá em **"Environment"**
6. Adicione a variável:
   ```
   DATABASE_URL = [COLE_A_URL_INTERNA_AQUI]
   ```

### 5. Deploy

1. Clique em **"Create Web Service"**
2. O Render iniciará o build automaticamente
3. Aguarde o deploy (pode demorar 3-5 minutos na primeira vez)

## 🌐 Seu Site Estará Disponível

- **URL Principal:** `https://caresense.onrender.com`
- **Admin Django:** `https://caresense.onrender.com/admin/`
- **Login Avaliadores:** `https://caresense.onrender.com/evaluators/login/`

## 🔧 O que Acontece Automaticamente

✅ **Instalação das dependências** Python  
✅ **Migração do banco** PostgreSQL  
✅ **Criação do superusuário** admin  
✅ **Coleta de arquivos estáticos**  
✅ **Configuração de segurança** HTTPS  
✅ **Configuração de domínio** automática

## Passo a Passo no Render

### 1. Criar Conta no Render
- Acesse [render.com](https://render.com)
- Faça login com GitHub/GitLab/Google

### 2. Conectar Repositório
- Clique em "New +"
- Selecione "Web Service"
- Conecte seu repositório GitHub/GitLab

### 3. Configurar Web Service
- **Name**: `caresense` (ou nome de sua escolha)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn caresense_project.wsgi:application`
- **Instance Type**: `Free` (para testes)

### 4. Configurar Variáveis de Ambiente
No painel do Render, adicione as variáveis:

```
DEBUG=false
SECRET_KEY=gere-uma-chave-secreta-aqui
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@caresense.com
DJANGO_SUPERUSER_PASSWORD=senha-segura-aqui
```

### 5. Criar Banco PostgreSQL (Recomendado)
- Clique em "New +"
- Selecione "PostgreSQL"
- **Name**: `caresense-db`
- **Database**: `caresense`
- **User**: `caresense`
- **Plan**: `Free`

### 6. Conectar Banco ao Web Service
- No seu Web Service, vá em "Environment"
- Adicione: `DATABASE_URL` = [URL do PostgreSQL criado]
- A URL estará disponível no painel do PostgreSQL

### 7. Deploy
- Clique em "Create Web Service"
- O deploy iniciará automaticamente

## Configurações Automáticas

O sistema configurará automaticamente:
- ✅ ALLOWED_HOSTS (via RENDER_EXTERNAL_HOSTNAME)
- ✅ CSRF_TRUSTED_ORIGINS
- ✅ Arquivos estáticos (WhiteNoise)
- ✅ Migrações do banco
- ✅ Criação de superusuário

## Acesso Pós-Deploy

1. **URL da aplicação**: `https://seu-app.onrender.com`
2. **Admin**: `https://seu-app.onrender.com/admin/`
3. **Login**: Use as credenciais do superusuário configurado

## Configurações Opcionais

### Custom Domain
- No painel do Render: "Settings" > "Custom Domains"

### Monitoramento
- "Settings" > "Health Check Path": `/`

### Logs
- Acesse "Logs" no painel para debug

## Troubleshooting

### Build Falha
- Verifique se `build.sh` está executável
- Confirme se `requirements.txt` está correto

### Database Error
- Verifique se `DATABASE_URL` está configurado
- Confirm se o PostgreSQL está ativo

### 403/404 Errors
- Verifique `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`
- Confirm `DEBUG=false` em produção

## Suporte
- Documentação Render: [render.com/docs](https://render.com/docs)
- Logs no painel do Render para debug
