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
release: python manage.py migrate --noinput
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

1. **Acesse**: https://railway.app/dashboard
2. **Crie novo projeto**: "Deploy from GitHub repo"
3. **Selecione**: brasiledu/CareSense.git
4. **Branch**: main

### 3. Configurar Variáveis de Ambiente

No painel do Railway, vá em **Variables** e adicione:

```env
SECRET_KEY=django-insecure-sua-chave-super-secreta-muito-longa-e-segura-aqui
DEBUG=false
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
```

### 4. Adicionar PostgreSQL

1. No dashboard do Railway
2. Clique em **"+ New"**
3. Selecione **"Database"** → **"PostgreSQL"**
4. A variável `DATABASE_URL` será criada automaticamente

### 5. Redeploy

Após configurar as variáveis, force um redeploy:
- Vá em **Deployments**
- Clique em **"Deploy Latest"**

## 🔍 Verificações Pós-Deploy

### 1. Migrações (Automáticas)
As migrações são executadas automaticamente pelo `Procfile`.

### 2. Arquivos Estáticos
```bash
# Se necessário, execute no Railway Shell:
python manage.py collectstatic --noinput
```

### 3. Criar Superusuário
```bash
# No Railway Shell:
python manage.py createsuperuser
```

## 🎯 URLs do Sistema

- **App**: `https://seu-projeto.up.railway.app/`
- **Admin**: `https://seu-projeto.up.railway.app/admin/`
- **Dashboard**: `https://seu-projeto.up.railway.app/dashboard/`

## ⚙️ Configurações de Segurança

O sistema está configurado para produção com:

- ✅ HTTPS obrigatório
- ✅ Cookies seguros
- ✅ Proteção XSS
- ✅ Proteção CSRF
- ✅ Headers de segurança
- ✅ WhiteNoise para arquivos estáticos

## 🐛 Troubleshooting

### Erro de ALLOWED_HOSTS
```python
# Adicione o domínio do Railway em ALLOWED_HOSTS
ALLOWED_HOSTS=*.railway.app,*.up.railway.app,seu-dominio.railway.app
```

### Erro de Static Files
```bash
# Execute no Railway Shell:
python manage.py collectstatic --noinput --clear
```

### Erro de Database
Verifique se o PostgreSQL foi adicionado e a variável `DATABASE_URL` existe.

## 📊 Monitoramento

O sistema inclui configurações para:
- Logs automáticos via `gunicorn`
- Compressão de arquivos estáticos
- Cache otimizado para produção

## 🔄 Atualizações

Para atualizações futuras:
1. Faça push para o repositório GitHub
2. O Railway fará redeploy automático
3. Migrações serão executadas automaticamente

---

**✅ Sistema pronto para produção no Railway!**
