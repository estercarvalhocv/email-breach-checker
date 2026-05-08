# Verificador de Vazamento de Emails

> **POC (Proof of Concept)** — Verificador simples de emails vazados usando a API gratuita do BreachDirectory.

## O que faz

Lê um arquivo `.txt` com uma lista de emails e consulta a API do [BreachDirectory](https://rapidapi.com/rohan-patra/api/breachdirectory) para verificar se cada email apareceu em algum vazamento de dados conhecido. Gera uma planilha Excel com o resultado.

## Requisitos

- **Python 3.10+**
- **Git** (opcional, para versionamento)
- **Conta no RapidAPI** (gratuita)

## Instalação

### 1. Clone o repositório (ou baixe os arquivos)

```bash
git clone git@github.com:estercarvalhocv/email-breach-checker.git
cd email-breach-checker
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # PowerShell
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key

1. Crie uma conta gratuita no [RapidAPI](https://rapidapi.com/auth/sign-up)
2. Acesse a [API do BreachDirectory](https://rapidapi.com/rohan-patra/api/breachdirectory) e subscreva ao plano **Basic (Free)** — 10 consultas/mês
3. Copie sua API Key
4. Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

5. Edite o `.env` e cole sua key:

```env
BREACHDIRECTORY_API_KEY=sua_api_key_aqui
```

## Uso

### 1. Prepare a lista de emails

Edite o arquivo `email.txt` com um email por linha:

```
teste@gmail.com
admin@empresa.com
contato@site.com.br
```

### 2. Execute o script

```bash
python main.py
```

### 3. Resultado

O script gera uma planilha `resultado_YYYYMMDD_HHMMSS.xlsx` com as colunas:

| Coluna | Descrição |
|---|---|
| `email` | Email consultado |
| `status` | `VAZADO`, `SEGURO` ou `ERRO` |
| `breaches` | Nome dos vazamentos encontrados |
| `data_consulta` | Data/hora da verificação |

E exibe um resumo no terminal:

```
==================================================
  RESULTADO
==================================================

  [!] teste@gmail.com
      Status: VAZADO
      Breaches: Adobe, LinkedIn

  [OK] admin@empresa.com
      Status: SEGURO

  Vazados: 1 | Seguros: 3 | Erros: 0
==================================================
```

## Estrutura do Projeto

```
email-breach-checker/
├── main.py              # Script principal
├── requirements.txt     # Dependências Python
├── .env.example         # Template de variáveis de ambiente
├── .env                 # Sua API Key (não commitar)
├── .gitignore           # Arquivos ignorados pelo git
└── email.txt            # Lista de emails para verificar
```

## Limitações

- **Free tier**: 10 consultas/mês no plano gratuito do RapidAPI
- **Delay**: 2 segundos entre requests para respeitar o rate limit
- **Escopo**: Apenas verificação de emails (CNPJ não implementado nesta POC)

## Licença

MIT
