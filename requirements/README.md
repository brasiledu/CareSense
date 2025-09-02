# Requirements

Esta pasta contém os arquivos de dependências Python organizados por ambiente.

## Arquivos

### `requirements-dev.txt`
Dependências para desenvolvimento, incluindo:
- Ferramentas de debug
- Linters e formatadores
- Bibliotecas de teste
- Dependências de desenvolvimento

### `requirements-prod.txt`
Dependências otimizadas para produção, incluindo:
- Apenas pacotes essenciais
- Servidor web (Gunicorn)
- Banco PostgreSQL
- Monitoramento e cache

## Uso

### Desenvolvimento
```bash
pip install -r requirements/requirements-dev.txt
```

### Produção
```bash
pip install -r requirements/requirements-prod.txt
```

### Nota
O arquivo `requirements.txt` na raiz do projeto é usado para desenvolvimento local e contém todas as dependências básicas.
