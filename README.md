# 📊 Monitor de Erros Power BI

Este projeto é um script Python (`monitor_email.py`) que monitora uma caixa de entrada de email (via IMAP) em busca de notificações de falha de atualização do Power BI. Quando um erro é detectado, ele envia um alerta imediato para um grupo ou chat no Telegram.

## 🚀 Funcionalidades

- **Monitoramento em Tempo Real:** Verifica a caixa de entrada a cada 60 segundos.
- **Filtro Inteligente:** Busca apenas emails com assuntos específicos (ex: "Erro no BI").
- **Alerta no Telegram:** Envia o assunto, remetente e um resumo do corpo do email para o Telegram.
- **Segurança:** Credenciais sensíveis são carregadas de um arquivo `.env` (não versionado).

## 🛠️ Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/DantasNx0/monitor-bi.git
    cd monitor-bi
    ```

2.  **Crie o ambiente virtual (Recomendado):**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuração

Crie um arquivo chamado `.env` na raiz do projeto e preencha com suas credenciais (use o arquivo `.env.example` como base se houver, ou siga o modelo abaixo):

```ini
# Credenciais do Email (Gmail/Outlook)
EMAIL_USER=seu_email@gmail.com
EMAIL_PASS=sua_senha_de_app_(nao_a_senha_normal)
IMAP_SERVER=imap.gmail.com

# Credenciais do Telegram
TELEGRAM_TOKEN=seu_token_do_bot
TELEGRAM_CHAT_ID=seu_chat_id

# Filtro
EMAIL_SUBJECT_FILTER=Erro no BI:
```

> **Nota:** Para Gmail, você deve usar uma "Senha de App" (App Password) e não sua senha de login.

## ▶️ Como Rodar

### Opção 1: Via Script (Windows)
Dê um duplo clique no arquivo **`INICIAR_MONITOR.bat`**.

### Opção 2: Via Terminal
```bash
python monitor_email.py
```

## 📦 Estrutura dos Arquivos

- `monitor_email.py`: Script principal.
- `requirements.txt`: Lista de bibliotecas Python necessárias.
- `.env`: Arquivo de configuração (NÃO COMPARTILHE).
- `INICIAR_MONITOR.bat`: Atalho para iniciar o monitor no Windows.
