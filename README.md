# Django Reset Migration

Este repositório oferece um script simples, seguro e interativo para **reinicializar migrações de um projeto Django** com múltiplos apps.

---

## Objetivo

Evitar o trabalho manual e repetitivo de apagar migrações uma a uma. Ideal para ambientes de desenvolvimento, projetos em estruturação ou ciclos rápidos de teste. Permite limpar a base e recriar migrações de forma automatizada, mantendo controle sobre cada etapa.

---

## Funcionalidades

- Remove a base de dados local (`db.sqlite3` por padrão)
- Apaga arquivos de migração (`*.py`, `*.pyc`), exceto `__init__.py`
- Detecta automaticamente todos os apps internos com pastas `migrations/`
- Executa `makemigrations` e `migrate` para recriar o esquema
- Instala automaticamente pacotes definidos no `requirements.txt`
- Modo interativo com confirmações antes de ações destrutivas

---

## Como usar

1. Clone este repositório **ou** copie o script `reset-migracoes.ps1` para a raiz do diretório do teu backend Django  
2. Certifica-te de que o ambiente virtual está **ativo**
3. Executa o script no terminal PowerShell:

```powershell
.\reset-migracoes.ps1
```
---

## Recomendado para
Desenvolvedores em fase inicial de projeto

Equipes que utilizam SQLite para desenvolvimento

Ambientes de formação, testes e protótipos

Times que prezam por clareza e controle no ciclo de desenvolvimento

---

## Avisos
Este script é pensado para uso local e ambientes de desenvolvimento.
Não é recomendado para produção ou ambientes com dados sensíveis.

Por padrão, a base db.sqlite3 será apagada.
Personalize o caminho no script conforme a estrutura do seu projeto.

