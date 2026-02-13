# 📊 Monitor de Erros Power BI / Fabric

Este projeto oferece **duas formas** de monitorar falhas de atualização em Datasets do Power BI e Microsoft Fabric, notificando via Telegram.

## 🚀 Funcionalidades

### 1. Novo Monitor via API (`monitor_fabric.py`)
> **Recomendado**
- **Monitoramento Proativo:** Varre automaticamente todos os Workspaces acessíveis via API REST.
- **Detecção Precisa:** Identifica falhas diretamente no histórico de atualização do dataset.
- **Inteligente:** Evita spam (notifica apenas uma vez por falha nova).
- **Intervalo:** Verifica a cada **10 minutos** (configurável).

### 2. Monitor via Email (`monitor_email.py`)
> **Lagado / Alternativo**
- **Reativo:** Monitora uma caixa de entrada IMAP (Gmail/Outlook) procurando por emails de erro enviados pelo Power BI.
- Ideal caso você não tenha permissões de admin/service principal, mas receba os emails de erro.

---

## 🛠️ Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/DantasNx0/monitor-bi.git
    cd monitor-bi
    ```

2.  **Crie o ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Configuração (.env)

Crie um arquivo chamado `.env` na raiz do projeto e preencha conforme o método escolhido:

### Para usar o Monitor API (`monitor_fabric.py`)
Você precisa de um **Service Principal** (App Registration) no Azure com acesso aos Workspaces.

```ini
# --- Credenciais do Power BI (Service Principal) ---
TENANT_ID=seu-tenant-id
CLIENT_ID=seu-client-id-do-app
CLIENT_SECRET=seu-client-secret-do-app
# ID de um Workspace de exemplo (opcional, usado apenas para testes)
WORKSPACE_ID=id-do-workspace

# --- Credenciais do Telegram ---
TELEGRAM_TOKEN=seu_token_do_bot
TELEGRAM_CHAT_ID=seu_chat_id
```

### Para usar o Monitor Email (`monitor_email.py`)
```ini
# --- Credenciais do Email (Gmail/Outlook) ---
EMAIL_USER=seu_email@gmail.com
EMAIL_PASS=sua_senha_de_app
IMAP_SERVER=imap.gmail.com
EMAIL_SUBJECT_FILTER=Refresh failed

# (Mantenha também as credenciais do Telegram acima)
```

---

## ▶️ Como Rodar

### Opção 1: Monitor via API (Recomendado)
No terminal:
```bash
python monitor_fabric.py
```
*Ele ficará rodando e verificará os workspaces a cada 10 minutos.*

### Opção 2: Monitor via Email
No terminal:
```bash
python monitor_email.py
```
*Ele ficará rodando e verificará a caixa de entrada a cada 60 segundos.*

---

## 📦 Estrutura dos Arquivos

- `monitor_fabric.py`: **[NOVO]** Script principal de monitoramento via API.
- `monitor_email.py`: Script legado de monitoramento via Email.
- `monitor_state.json`: Arquivo automático para gerenciar estado e evitar notificações duplicadas.
- `.env`: Arquivo de configuração de senhas (NÃO COMPARTILHE).
- `requirements.txt`: Dependências do Python (`requests`, `python-dotenv`).
