# CareSense

Sistema de Avaliação Neuropsicológica desenvolvido para auxiliar profissionais de saúde na aplicação e análise de testes cognitivos padronizados.

## Descrição

O CareSense é uma plataforma web desenvolvida em Django que permite a aplicação, armazenamento e análise de avaliações neuropsicológicas. O sistema oferece uma interface otimizada para tablets, facilitando a aplicação de testes em ambiente clínico.

## Funcionalidades

### Gestão de Pacientes
- Cadastro completo de pacientes com dados demográficos
- Histórico de avaliações por paciente
- Busca e filtros avançados

### Avaliações Neuropsicológicas
- **Digit Span Test**: Avaliação da memória de trabalho
- **Trail Making Test (TMT)**: Avaliação de atenção e flexibilidade cognitiva
- **Stroop Test**: Avaliação do controle inibitório

### Análise Estatística
- Cálculo automático de Z-scores baseados em dados normativos
- Relatórios de risco cognitivo
- Dashboard com indicadores de performance

### Interface de Usuário
- Design responsivo otimizado para tablets
- Interface intuitiva para aplicação de testes
- Visualização de dados com gráficos interativos

## Requisitos do Sistema

### Software
- Python 3.8 ou superior
- Django 4.2.14
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Hardware Recomendado
- Tablet com tela de 10" ou superior
- Processador quad-core
- 4GB RAM mínimo
- Conexão com internet estável

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/caresense.git
cd caresense
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
python manage.py migrate
```

### 5. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

O sistema estará disponível em `http://localhost:8000`

## Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua-chave-secreta-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Banco de Dados
Por padrão, o sistema utiliza SQLite para desenvolvimento. Para produção, recomenda-se PostgreSQL.

## Estrutura do Projeto

```
caresense-project/
├── apps/
│   ├── core/           # Funcionalidades principais
│   ├── patients/       # Gestão de pacientes
│   ├── assessments/    # Avaliações neuropsicológicas
│   └── users/          # Gestão de usuários
├── caresense_project/  # Configurações do Django
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos (CSS, JS)
├── manage.py          # Script de gerenciamento Django
└── requirements.txt   # Dependências do projeto
```

## APIs Disponíveis

O sistema oferece APIs REST para integração:

### Pacientes
- `GET /api/patients/` - Lista todos os pacientes
- `POST /api/patients/` - Cria novo paciente
- `GET /api/patients/{id}/` - Detalhes de um paciente

### Avaliações
- `GET /api/assessments/` - Lista todas as avaliações
- `POST /api/assessments/` - Cria nova avaliação
- `GET /api/assessments/{id}/` - Detalhes de uma avaliação

## Testes Implementados

### Digit Span Test
- Avalia memória de trabalho verbal
- Variantes: span direto e inverso
- Cálculo automático de Z-score

### Trail Making Test
- Parte A: atenção sustentada
- Parte B: flexibilidade cognitiva
- Medição de tempo e erros

### Stroop Test
- Três cartões de aplicação
- Avaliação do controle inibitório
- Análise de tempo de interferência

## Dados Normativos

O sistema utiliza dados normativos baseados em:
- Idade do paciente
- Nível de escolaridade
- População brasileira

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## Changelog

### Versão 1.0.0 (2025-08-07)
- Implementação inicial do sistema
- Testes neuropsicológicos básicos
- Interface web responsiva
- Sistema de Z-scores
- Dashboard de análise
