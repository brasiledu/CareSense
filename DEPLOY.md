# 🚀 Deploy do AvivaMente no Railway

## Preparação Completa para Produção

Este guia contém todas as instruções para fazer deploy do sistema AvivaMente no Railway.

## 📋 Pré-requisitos

- [x] Projeto configurado no GitHub
- [x] Conta no Railway (https://railway.app)
- [x] Arquivos de configuração criados

## 🔧 Arquivos de Deploy Criados

### 1. `Procfile`
```
web: gunicorn caresense_project.wsgi --log-file -
```

### 2. `runtime.txt`
```
python-3.11.6
```

### 3. `.railway.json`
Configurações específicas do Railway para build e deploy.

### 4. `requirements-prod.txt`
Dependências otimizadas para produção incluindo:
- `gunicorn` - Servidor WSGI
- `whitenoise` - Arquivos estáticos
- `psycopg2-binary` - PostgreSQL
- `dj-database-url` - URL de database

## 🚀 Passos para Deploy

### 1. Push das Alterações
```bash
git add .
git commit -m "feat: configuração completa para deploy no Railway"
git push origin main
```

### 2. Configurar no Railway

1. Acesse: https://railway.app/dashboard
2. Crie novo projeto: Deploy from GitHub repo
3. Selecione o repositório
4. Branch: main

### 3. Configurar Variáveis de Ambiente

No painel do Railway, em Variables, adicione:

```env
SECRET_KEY=django-insecure-sua-chave-super-secreta-muito-longa-e-segura-aqui
DEBUG=false
ALLOWED_HOSTS=*.railway.app,*.up.railway.app,SEU_SUBDOMINIO.up.railway.app
CSRF_TRUSTED_ORIGINS=https://SEU_SUBDOMINIO.up.railway.app,https://*.railway.app,https://*.up.railway.app
```

Observações:
- Se usar domínio próprio, inclua-o nas duas variáveis (com https:// para CSRF_TRUSTED_ORIGINS).
- Em produção, os cookies usam SameSite=Lax por padrão.

### 4. Adicionar PostgreSQL

1. No dashboard do Railway
2. Clique em + New
3. Selecione Database → PostgreSQL
4. A variável DATABASE_URL será criada automaticamente

### 5. Redeploy

Após configurar as variáveis, force um redeploy:
- Vá em Deployments
- Clique em Deploy Latest

## 🔍 Verificações Pós-Deploy

### 1. Migrações
Execute no Shell do Railway (deploy iniciado com sucesso):
```bash
python manage.py migrate --noinput
```

### 2. Arquivos Estáticos
```bash
python manage.py collectstatic --noinput --clear
```

### 3. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 4. Healthcheck
- Endpoint público: https://SEU_SUBDOMINIO.up.railway.app/healthz/
- Configurado em `.railway.json`

## 🎯 URLs do Sistema

- App: https://SEU_SUBDOMINIO.up.railway.app/
- Admin: https://SEU_SUBDOMINIO.up.railway.app/admin/
- Dashboard: https://SEU_SUBDOMINIO.up.railway.app/dashboard/

## ⚙️ Configurações de Segurança

- Proxy SSL: SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')
- Headers: XSS e content type nosniff ativados
- CSRF_TRUSTED_ORIGINS configurável via variável de ambiente
- WhiteNoise para estáticos com Manifest e compressão

## 🐛 Troubleshooting

### 403 CSRF no login
- Confirme CSRF_TRUSTED_ORIGINS com o domínio exato (https://...)
- Confirme que o template tem `{% csrf_token %}` (login.html já tem)
- Limpe sessões antigas: `python manage.py clearsessions`
- Verifique se DEBUG=false em produção

### DisallowedHost
- Inclua o host exato do Railway em ALLOWED_HOSTS (sem espaços)

### Erro de Static Files
```bash
python manage.py collectstatic --noinput --clear
```

### Erro de Database
- Verifique se o PostgreSQL foi adicionado e a variável DATABASE_URL existe.

## 📊 Monitoramento

- Logs via gunicorn (Procfile)
- Compressão de estáticos via WhiteNoise

## 🔄 Atualizações

1. Push para o GitHub
2. Railway faz redeploy
3. Rode migrate/collectstatic no Shell se necessário

---

✅ Sistema pronto para produção no Railway
