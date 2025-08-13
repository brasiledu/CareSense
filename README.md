# AvivaMente

Sistema de Avaliação Neuropsicológica desenvolvido para auxiliar profissionais de saúde na aplicação e análise de testes cognitivos padronizados.

## Descrição

O AvivaMente é uma plataforma web desenvolvida em Django que permite a ### Versão 1.2.0 (2025-01-13)
- Reorganização completa da estrutura de templates por módulos
- Melhoria na manutenibilidade e organização do código
- Atualização automática de todas as referências nos views
- Estrutura mais limpa e escalável

### Versão 1.1.0 (2025-01-13)
- Refinamento do Teste de Stroop com matriz 5x5 responsiva
- Aplicação da identidade visual do projeto AvivaMente
- Remoção de emojis e padronização de ícones Font Awesome
- Interface modernizada com design system consistente
- Melhorias de responsividade para tablets e mobile

### Versão 1.0.0 (2025-01-07)azenamento e análise de avaliações neuropsicológicas. O sistema oferece uma interface moderna e responsiva, otimizada para tablets e diferentes dispositivos, facilitando a aplicação de testes em ambiente clínico.

## Funcionalidades

### Gestão de Pacientes
- Cadastro completo de pacientes com dados demográficos
- Histórico de avaliações por paciente com gráficos de evolução
- Busca e filtros avançados
- Dashboard individualizado de performance

### Avaliações Neuropsicológicas
- **Digit Span Test**: Avaliação da memória de trabalho (versão interativa e simplificada)
- **Trail Making Test (TMT)**: Avaliação de atenção e flexibilidade cognitiva
- **Stroop Test**: Avaliação do controle inibitório (matriz 5x5 responsiva)

### Análise Estatística Avançada
- Cálculo automático de Z-scores baseados em dados normativos brasileiros
- Sistema de cálculo de risco cognitivo em múltiplos níveis (LOW, MODERATE, HIGH, CRITICAL)
- Relatórios detalhados de performance
- Dashboard com indicadores visuais e gráficos interativos

### Interface Moderna
- Design system consistente com identidade visual do projeto
- Interface responsiva otimizada para tablets, desktop e mobile
- Cards modernos com sombras e bordas arredondadas
- Ícones Font Awesome para melhor UX
- Navegação intuitiva e fluxo otimizado

## Melhorias Recentes Implementadas

### Organização de Templates (v1.2.0)
- Reestruturação completa da pasta templates por módulos:
  - `templates/assessments/` - Templates de avaliações e testes
  - `templates/patients/` - Templates de pacientes
  - `templates/users/` - Templates de usuários e autenticação
  - `templates/core/` - Templates principais (dashboard, home)
- Atualização automática de todas as referências nos views
- Melhoria na manutenibilidade e organização do código

### Refinamento do Teste Stroop (v1.1.0)
- Redução de 50 para 25 estímulos em matriz 5x5 responsiva
- Interface modernizada com design system consistente
- Remoção de emojis e aplicação da identidade visual do projeto
- Timer aprimorado com ícones Font Awesome
- Controles reorganizados para melhor usabilidade
- Responsividade completa para diferentes tamanhos de tela

### Sistema de Z-scores Aprimorado
- Implementação de dados normativos específicos para população brasileira
- Cálculo preciso baseado em idade e escolaridade
- Sistema de validação e fallback para casos especiais
- Relatórios detalhados de interpretação clínica

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
git clone https://github.com/seu-usuario/avivamende.git
cd avivamende
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
Por padrão, o sistema utiliza SQLite para desenvolvimento. Para produção, recomenda-se PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'avivamende_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Estrutura do Projeto (Reorganizada)

```
caresense-project/
├── apps/
│   ├── core/           # Funcionalidades principais (dashboard, home)
│   ├── patients/       # Gestão de pacientes
│   ├── assessments/    # Avaliações neuropsicológicas
│   └── users/          # Gestão de usuários
├── caresense_project/  # Configurações do Django
├── evaluators/         # Módulo de avaliadores
├── templates/          # Templates organizados por módulo
│   ├── assessments/    # Templates de testes e avaliações
│   ├── patients/       # Templates de pacientes
│   ├── users/          # Templates de usuários
│   └── core/           # Templates principais
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
- Avalia memória de trabalho verbal e numérica
- Variantes: span direto e inverso
- Versões interativa e simplificada disponíveis
- Cálculo automático de Z-score baseado em normas brasileiras

### Trail Making Test
- Parte A: atenção sustentada e velocidade de processamento
- Parte B: flexibilidade cognitiva e função executiva
- Medição precisa de tempo e contagem de erros
- Interface moderna com cronômetro visual

### Stroop Test (Versão Otimizada)
- Três cartões de aplicação em matriz 5x5 (25 estímulos cada)
- Cartão 1: Nomeação de cores (retângulos coloridos)
- Cartão 2: Leitura de palavras (palavras em preto)
- Cartão 3: Interferência Stroop (palavras coloridas incongruentes)
- Interface responsiva com timer automático
- Sistema de registro de erros em tempo real

## Dados Normativos Brasileiros

O sistema utiliza dados normativos específicos baseados em:
- Idade do paciente (faixas etárias: 18-39, 40-59, 60-79, 80+)
- Nível de escolaridade (anos de estudo)
- População brasileira com validação científica
- Tabelas de conversão Z-score por teste cognitivo

## Tecnologias Utilizadas

### Backend
- Python 3.8+
- Django 4.2.14
- SQLite (desenvolvimento) / PostgreSQL (produção)
- Django REST Framework (APIs)

### Frontend
- HTML5 / CSS3
- JavaScript (ES6+)
- Font Awesome Icons
- Chart.js (gráficos)
- Design system responsivo

### Funcionalidades Avançadas
- Sistema de Z-scores normativos
- Cálculo de risco cognitivo automático
- Dashboard com visualizações interativas
- Interface otimizada para tablets
- Sistema de relatórios detalhados

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## Suporte

Para suporte técnico ou dúvidas sobre o uso do sistema:
- Email: suporte@avivamende.com
- Documentação: https://docs.avivamende.com

## Changelog

### Versão 1.2.0 (2025-08-13)
- Reorganização completa da estrutura de templates por módulos
- Melhoria na manutenibilidade e organização do código
- Atualização automática de todas as referências nos views
- Estrutura mais limpa e escalável

### Versão 1.1.0 (2025-08-13)
- Refinamento do Teste de Stroop com matriz 5x5 responsiva
- Aplicação da identidade visual do projeto AvivaMende
- Remoção de emojis e padronização de ícones Font Awesome
- Interface modernizada com design system consistente
- Melhorias de responsividade para tablets e mobile

### Versão 1.0.0 (2025-08-07)
- Implementação inicial do sistema
- Testes neuropsicológicos básicos (Digit Span, TMT, Stroop)
- Interface web responsiva
- Sistema de Z-scores com dados normativos brasileiros
- Dashboard de análise com gráficos interativos

## Roadmap

### Próximas Funcionalidades
- Integração com HL7 FHIR para interoperabilidade
- Exportação de relatórios em PDF
- Novos testes neuropsicológicos (MMSE, Fluência Verbal)
- Aplicativo mobile nativo
- Sistema de backup automático
- Módulo de agendamento de avaliações
- Sistema de notificações e lembretes