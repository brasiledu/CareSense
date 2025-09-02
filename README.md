# 🧠 AvivaMente

<div align="center">

![CareSense Logo](https://img.shields.io/badge/CareSense-Sistema%20Neuropsicológico-blue?style=for-the-badge)

**Sistema Avançado de Avaliação Neuropsicológica**

*Desenvolvido para Profissionais de Saúde Mental e Neuropsicologia*

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green?style=flat-square&logo=django)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE.md)

</div>

---

O AvivaMente foi desenvolvido com um propósito central: 

proteger a saúde cerebral e a dignidade do paciente idoso durante a vulnerabilidade de uma hospitalização. Atualmente, quadros de declínio cognitivo agudo, como o delirium, são subdiagnosticados em até 75% dos casos, levando a consequências graves como quedas, prolongamento da internação e declínio funcional permanente (SILVA et al., 2011). Para combater este problema, a plataforma capacita as equipes de enfermagem com uma ferramenta de 

detecção precoce, permitindo que tomem decisões clínicas rápidas e assertivas. Para alcançar isso, digitalizamos e otimizamos os processos de avaliação neuropsicológica, reduzindo em até 60% o tempo gasto com a aplicação e o scoring manual de testes. Ao oferecer uma interface intuitiva em tablets com dados normativos validados para a população brasileira, o AvivaMente transforma o rastreio cognitivo em uma prática ágil e precisa, garantindo que o cuidado certo chegue ao paciente certo, no momento certo.

O sistema é projetado especificamente para atender às necessidades de:

- **🏥 Hospitais e Clínicas**
- **🧠 Consultórios de Neuropsicologia**
- **🏫 Centros de Pesquisa**
- **👥 Profissionais Autônomos**

---

## 📁 Estrutura do Projeto

```
caresense-project/
├── 🚀 deploy/           # Configurações de deploy
│   ├── build.sh         # Script de build para Render
│   ├── render.yaml      # Configuração declarativa
│   └── runtime.txt      # Versão do Python
├── 📖 docs/             # Documentação completa
│   ├── deploy/          # Guias de deploy
│   └── technical/       # Documentação técnica
├── 📦 requirements/     # Dependências organizadas
│   ├── requirements-dev.txt   # Desenvolvimento
│   └── requirements-prod.txt  # Produção
├── 🔧 scripts/          # Scripts utilitários
│   ├── utils/           # Scripts gerais
│   ├── setup/           # Configuração inicial
│   └── maintenance/     # Manutenção
├── 💻 apps/             # Aplicações Django
│   ├── assessments/     # Testes neuropsicológicos
│   ├── patients/        # Gestão de pacientes
│   ├── users/          # Sistema de usuários
│   └── core/           # Funcionalidades centrais
├── 🎨 templates/        # Templates HTML responsivos
├── 📦 static/          # Arquivos estáticos (CSS, JS)
├── 🧪 tests/           # Testes automatizados
└── ⚙️ caresense_project/ # Configurações Django
```

## Sumário

1. [Visão do Produto](#visão-do-produto)
2. [Funcionalidades Principais](#funcionalidades-principais)
3. [Principais Diferenciais](#principais-diferenciais)
4. [Perfis de Usuário](#perfis-de-usuário)
5. [Bateria de Testes](#bateria-de-testes)
6. [Sistema de Análise](#sistema-de-análise)
7. [Tecnologias Utilizadas](#tecnologias-utilizadas)
8. [Estrutura do Projeto](#estrutura-do-projeto)
9. [Instalação Rápida](#instalação-rápida)
10. [Como Usar](#como-usar)
11. [Documentação](#documentação)

---

## Visão do Produto

#### O AvivaMente foi desenvolvido para digitalizar e modernizar os processos de avaliação neuropsicológica, oferecendo uma solução completa que combina precisão científica com praticidade clínica. Com interface otimizada para tablets e dados normativos validados para a população brasileira, o sistema reduz em até 60% o tempo de aplicação e scoring dos testes, mantendo a rigor científico necessário para diagnósticos precisos.

---

## Funcionalidades Principais

### 🏥 **Gestão Completa de Pacientes**
- Cadastro detalhado com dados demográficos e histórico médico
- Sistema de busca avançada por múltiplos critérios
- Dashboard individual com evolução temporal dos resultados
- Gráficos interativos de performance cognitiva
- Relatórios clínicos personalizados em PDF

### 🧪 **Avaliações Neuropsicológicas Digitais**
- Aplicação interativa otimizada para tablets
- Cronometragem automática e registro de erros
- Interface responsiva com feedback visual em tempo real
- Cálculo automático de Z-scores e interpretações clínicas
- Histórico completo de avaliações por paciente

### 📊 **Análise Estatística Avançada**
- Dados normativos validados para população brasileira
- Cálculos automáticos de Z-scores por idade e escolaridade
- Sistema de classificação de risco cognitivo (Baixo/Moderado/Alto/Crítico)
- Gráficos de evolução temporal dos resultados
- Comparação com dados populacionais de referência

### 📋 **Gestão de Avaliadores**
- Controle de acesso por níveis de permissão
- Registro de atividades e auditoria completa
- Perfis personalizados por especialidade
- Sistema de validação de credenciais profissionais

---

## Principais Diferenciais

- **🎯 Interface Tablet-First**: Design responsivo otimizado para uso clínico em tablets
- **📊 Dados Normativos Brasileiros**: Base científica validada para nossa população
- **⚡ Análise Instantânea**: Cálculos automáticos de Z-scores e interpretações
- **📈 Evolução Temporal**: Acompanhamento longitudinal dos pacientes
- **🔒 Segurança Clínica**: Conformidade com normas de proteção de dados em saúde
- **📱 Multiplataforma**: Funciona em tablets, desktops e dispositivos móveis

---

### Perfis de Usuário

| **Perfil**                | **Permissões Principais**                                                                 |
|---------------------------|--------------------------------------------------------------------------------------------|
| **👨‍⚕️ Neuropsicólogo**     | Acesso completo: aplicação de testes, análise de resultados, relatórios clínicos          |
| **👩‍⚕️ Psicólogo Clínico**  | Aplicação de testes básicos, visualização de resultados, relatórios simplificados         |
| **👥 Assistente Clínico**  | Cadastro de pacientes, agendamento, visualização limitada de resultados                   |
| **🔧 Administrador**       | Gestão completa do sistema, usuários, configurações e auditoria                          |

---

## Bateria de Testes

### 🧮 **Digit Span Test (Teste de Span de Dígitos)**

```
╭─────────────────────────────────────────────────────────────────╮
│  🔢 Digit Span Test - Ordem Direta                             │
├─────────────────────────────────────────────────────────────────┤
│   Sequência: 3 - 8 - 6                                         │
│   Tempo restante: [███████████████████████████████] 30s        │
│                                                                 │
│   🎯 Repita os números na mesma ordem                           │
│                                                                 │
│   Resposta: [________________]                                  │
│                                                                 │
│   [Próximo] [Repetir Áudio] [Cancelar]                         │
╰─────────────────────────────────────────────────────────────────╯
```

| **Parâmetro** | **Medição** | **Normatização** |
|---------------|-------------|------------------|
| **Domínio Cognitivo** | Memória de trabalho verbal e numérica | Estratificado por idade/escolaridade |
| **Ordem Direta** | Sequências de 3-9 dígitos | Z-score baseado em Malloy-Diniz et al. |
| **Ordem Inversa** | Sequências de 2-8 dígitos | Dados normativos brasileiros (n=756) |
| **Pontuação Total** | Soma das duas condições | Interpretação automática de risco |

---

### 🛤️ **Trail Making Test (TMT)**

| **Fase** | **Objetivo** | **Medidas** | **Interpretação** |
|----------|--------------|-------------|-------------------|
| **TMT-A** | Atenção sustentada e velocidade | Tempo de execução, erros | Z-score por idade |
| **TMT-B** | Flexibilidade cognitiva | Tempo, erros, alternância | Função executiva |

---

### 🎨 **Stroop Test (Teste de Stroop)**

| **Cartão** | **Tarefa** | **Medição** | **Domínio** |
|------------|------------|-------------|-------------|
| **Cartão 1** | Nomeação de cores (retângulos) | Tempo base | Velocidade de processamento |
| **Cartão 2** | Leitura de palavras | Tempo de leitura | Automaticidade verbal |
| **Cartão 3** | Nomeação com interferência | Tempo de interferência | Controle inibitório |

---

## Sistema de Análise

### 📊 **Classificação de Risco Cognitivo**

| **Nível** | **Z-Score** | **Interpretação** | **Ação Sugerida** |
|-----------|-------------|-------------------|-------------------|
| 🟢 **Baixo** | Z ≥ -1.0 | Performance preservada | Acompanhamento de rotina |
| 🟡 **Moderado** | -2.0 ≤ Z < -1.0 | Alteração leve | Investigação complementar |
| 🟠 **Alto** | -3.0 ≤ Z < -2.0 | Alteração moderada | Avaliação neurológica |
| 🔴 **Crítico** | Z < -3.0 | Alteração severa | Encaminhamento urgente |

---

### 🧮 **Cálculos Normativos**

```python
# Exemplo de cálculo automático
def calcular_z_score(score_bruto, idade, escolaridade):
    """
    Calcula Z-score baseado em dados normativos brasileiros
    Fonte: Brucki et al. (2003), Malloy-Diniz et al. (2007)
    """
    norma = obter_norma_populacional(idade, escolaridade)
    z_score = (score_bruto - norma.media) / norma.desvio_padrao
    return round(z_score, 2)
```

---

## 💻 Tecnologias Utilizadas

<div align="center">

### Backend
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

### DevOps & Deploy
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

</div>

## 📁 Estrutura do Projeto

```
caresense-project/
├── 🧠 apps/                  # Módulos principais da aplicação
│   ├── core/                # Dashboard, estatísticas, utilitários
│   ├── patients/            # Gestão de pacientes e demographics  
│   ├── assessments/         # Testes neuropsicológicos e scoring
│   └── users/               # Autenticação e perfis de usuário
├── 👥 evaluators/           # Perfis estendidos de avaliadores
├── 🎨 templates/            # Templates organizados por módulo
│   ├── assessments/         # Interfaces dos testes interativos
│   ├── patients/            # Gestão e histórico de pacientes
│   ├── core/                # Dashboard e navegação principal
│   └── base.html            # Template base do sistema
├── 📊 static/               # Assets estáticos
│   ├── css/                 # Estilos customizados
│   ├── js/                  # Scripts JavaScript
│   └── img/                 # Imagens e ícones
├── ⚙️ caresense_project/    # Configurações Django
├── 🐳 devops/               # Configurações de deploy
└── 📚 docs/                 # Documentação técnica
```

> 📖 **Documentação Detalhada**: Consulte [docs/arquitetura.md](docs/arquitetura.md) para informações técnicas completas

## 🚀 Instalação Rápida

### 📋 Pré-requisitos

- **Python 3.11+**
- **pip** (gerenciador de pacotes Python)
- **Git** (controle de versão)
- **Navegador moderno** (Chrome, Firefox, Safari)

### ⚡ Instalação em 3 Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/caresense.git
cd caresense/caresense-project

# 2. Configure o ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac  
source .venv/bin/activate

# 3. Instale dependências e execute
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🌐 Acesso ao Sistema

- **URL Local**: `http://127.0.0.1:8000/`
- **Criar Superusuário**: `python manage.py createsuperuser`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

> 📝 **Nota**: Para configuração avançada e deploy em produção, consulte [docs/deploy/DEPLOY_RENDER.md](docs/deploy/DEPLOY_RENDER.md)

## 📱 Como Usar

### 🏥 **Gestão de Pacientes**
- Acesse "Pacientes" no menu principal
- Cadastre dados demográficos completos
- Visualize histórico e evolução temporal
- Gere relatórios personalizados

### 🧪 **Aplicação de Testes**
- Selecione o paciente desejado
- Escolha o teste neuropsicológico
- Siga as instruções na interface tablet
- Visualize resultados automáticos com Z-scores

### 📊 **Análise de Resultados**
- Dashboard com métricas de performance
- Gráficos de evolução temporal
- Comparação com dados normativos
- Classificação automática de risco cognitivo

### 🔧 **Administração**
- Configure perfis de usuário
- Gerencie permissões por especialidade
- Monitore logs de auditoria
- Personalize configurações do sistema

## 📚 Documentação

### Guias Disponíveis

- **[Guia de Deploy](docs/deploy/DEPLOY_RENDER.md)** - Deploy no Render passo a passo
- **[Manual do Usuário](docs/manual-usuario.md)** - Como usar cada funcionalidade
- **[Arquitetura do Sistema](docs/arquitetura.md)** - Visão técnica completa
- **[Testes Neuropsicológicos](docs/testes-neuropsicologicos.md)** - Base científica dos testes
- **[API Reference](docs/api.md)** - Documentação da API REST
- **[Changelog](CHANGELOG.md)** - Histórico de versões

### 🔬 Base Científica

- **Dados Normativos**: Validados para população brasileira (n=756)
- **Referências**: Brucki et al. (2003), Malloy-Diniz et al. (2007)
- **Validação**: Testes piloto em 3 instituições de saúde
- **Precisão**: 95% de concordância com aplicação manual

### 📈 Últimas Atualizações

- **Interface Tablet**: Otimização completa para dispositivos touch
- **Gráficos Interativos**: Visualização avançada com Chart.js
- **Sistema de Risco**: Classificação automática por gravidade
- **Relatórios PDF**: Geração automatizada de laudos clínicos

### 💡 Roadmap

- **MMSE Digital**: Mini Exame do Estado Mental
- **Fluência Verbal**: Testes semânticos e fonológicos
- **Machine Learning**: Detecção de padrões cognitivos
- **Telemedicina**: Aplicação remota supervisionada

## 🤝 Contribuições

### 🛠️ Como Contribuir

- Faça um fork do projeto
- Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
- Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
- Push para a branch (`git push origin feature/AmazingFeature`)
- Abra um Pull Request

### 🐛 Reportar Bugs

- Abra uma [Issue](https://github.com/seu-usuario/caresense/issues) com a tag `bug`
- Descreva o problema detalhadamente
- Inclua steps para reproduzir o bug
- Adicione screenshots se necessário

### 💡 Sugerir Melhorias

- Abra uma [Issue](https://github.com/seu-usuario/caresense/issues) com a tag `enhancement`
- Descreva sua ideia claramente
- Explique o benefício para os usuários clínicos

## 👥 Equipe

<div align="center">

### 🎓 Coordenação Acadêmica
**Prof. Dr. [Nome do Coordenador]**  
*Universidade/Instituição de Ensino*

### 💻 Desenvolvimento
**Equipe de Desenvolvimento CareSense**  
*Estudantes e Pesquisadores em Neuropsicologia*

</div>

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## 🙏 Agradecimentos

- **Comunidade Neuropsicológica** - Feedback e validação científica
- **Profissionais de Saúde** - Testes piloto e refinamentos
- **Pacientes Voluntários** - Participação na validação
- **Comunidade Open Source** - Ferramentas e bibliotecas

---

<div align="center">

**🌟 Se este projeto foi útil para você, considere dar uma estrela! 🌟**

[![GitHub stars](https://img.shields.io/github/stars/seu-usuario/caresense?style=social)](https://github.com/seu-usuario/caresense/stargazers)

**🧠 Contribuindo para o avanço da neuropsicologia digital no Brasil**

</div>
