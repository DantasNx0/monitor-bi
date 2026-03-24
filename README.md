# 📊 Monitor de Erros Power BI / Fabric

Este projeto oferece **duas formas** de monitorar falhas de atualização em Datasets do Power BI e Microsoft Fabric, notificando via Telegram.

## 🚀 Funcionalidades

### 1. Novo Monitor via API (`monitor_fabric.py`)
> **Recomendado**
- **Monitoramento Proativo:** Varre automaticamente todos os Workspaces acessíveis via API REST.
- **Detecção Precisa:** Identifica falhas diretamente no histórico de atualização do dataset.
- **Inteligente:** Evita spam (notifica apenas uma vez por falha nova).
- **Resiliente:** Conta com sistema automático de retentativas (Retry/Backoff) para tolerar micro-quedas de internet sem falsos positivos.
- **Intervalo:** Verifica a cada **10 minutos** (configurável).

### 2. Monitor via Email (`monitor_email.py`)
> **Legado / Alternativo**
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

### Opção 1: Monitor via API (Acompanhando pelo Terminal)
Para ver os logs rodando ao vivo na tela de comando negra:
```bash
python monitor_fabric.py
```
*(Ou dê um clique duplo em `INICIAR_MONITOR.bat`)*

### Opção 2: Monitor via API (Modo Oculto 24/7)
Para que o bot rode invisível em segundo plano sem abrir nenhuma "tela preta" que pode ser fechada por acidente:
- Dê um **clique duplo** no arquivo `RODAR_OCULTO.vbs`. 
- *(Dica: Coloque um atalho desse arquivo na pasta `shell:startup` do Windows para o robô iniciar automaticamente quando o PC ligar).*

### Opção 3: Monitor via Email (Legado)
No terminal:
```bash
python monitor_email.py
```

---

## 📦 Estrutura dos Arquivos

- `monitor_fabric.py`: **[PRINCIPAL]** Script de monitoramento via API com resiliência de conexão.
- `RODAR_OCULTO.vbs`: Script que inicia o `monitor_fabric.py` totalmente background (invisível).
- `INICIAR_MONITOR.bat`: Atalho para abrir a execução com a visualização clássica no terminal.
- `monitor_email.py`: Script legado de monitoramento via Email IMAP.
- `monitor_state.json`: Arquivo automático (gerado pelo sistema) para controlar o envio de Alertas no Telegram.
- `.env`: Arquivo de configuração de chaves secretas (NÃO COMPARTILHE NO GITHUB).
- `requirements.txt`: Dependências essenciais do pacote Python.
