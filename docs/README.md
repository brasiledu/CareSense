# 📖 Documentação do CareSense

Esta pasta contém toda a documentação técnica e de desenvolvimento do projeto CareSense.

## 📋 Índice de Documentos

### 🚀 Deploy e Configuração
- [`DEPLOY.md`](./DEPLOY.md) - Instruções de deploy e configuração do ambiente de produção

### 🧠 Implementações de Testes Neuropsicológicos
- [`MEEM_ETAPA_4_CONCLUIDA.md`](./MEEM_ETAPA_4_CONCLUIDA.md) - Documentação da implementação do Mini Exame do Estado Mental

## 📚 Documentação por Funcionalidade

### ✅ Testes Neuropsicológicos Implementados
1. **MEEM (Mini Exame do Estado Mental)** - Teste completo de triagem cognitiva
2. **Clock Drawing Test** - Teste do desenho do relógio para avaliação cognitiva
3. **Digit Span Test** - Teste de amplitude de dígitos para memória de trabalho
4. **TMT (Trail Making Test)** - Teste de trilhas para funções executivas
5. **Stroop Test** - Teste de interferência para atenção e controle inibitório

### 🔄 Em Desenvolvimento
- Montreal Cognitive Assessment (MoCA)
- Teste de Fluência Verbal
- Addenbrooke's Cognitive Examination (ACE-R)

## 🏗️ Arquitetura do Sistema

O CareSense é desenvolvido em Django com arquitetura modular:

- **Frontend**: Templates responsivos com Bootstrap e JavaScript
- **Backend**: Django REST Framework para APIs
- **Database**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Deploy**: Docker + Render.com

## 📝 Convenções de Documentação

- Todos os novos testes neuropsicológicos devem ter sua documentação específica
- Incluir screenshots da interface quando relevante
- Documentar mudanças na estrutura do banco de dados
- Manter histórico de versões e melhorias

---
*Última atualização: Agosto 2025*
