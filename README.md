# 📊 Monitor de Erros Power BI / Fabric

Este projeto oferece uma forma automatizada e invisível de monitorar falhas de atualização em Datasets do Power BI e Microsoft Fabric, notificando sua equipe diretamente via Telegram.

## 🚀 Funcionalidades

- **Monitoramento Proativo:** Varre automaticamente todos os Workspaces acessíveis via API REST.
- **Detecção Precisa:** Identifica falhas diretamente no histórico de atualização dos datasets.
- **Inteligente:** Evita spam, notificando apenas uma vez para cada falha nova.
- **Resiliente:** Conta com sistema automático de retentativas (Retry/Backoff) para tolerar micro-quedas de internet sem gerar alarmes falsos.
- **Background / Invisível:** Script pronto para execução totalmente oculta 24/7, sem travamento de janelas na tela.
- **Intervalo:** Verifica automaticamente os datasets a cada **10 minutos** por padrão.

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

Crie um arquivo chamado `.env` na raiz do projeto contendo as credenciais do **Service Principal** (App Registration) da sua conta Azure, junto os Dados do Telegram:

```ini
# --- Credenciais do Power BI (Service Principal) ---
TENANT_ID=seu-tenant-id
CLIENT_ID=seu-client-id-do-app
CLIENT_SECRET=seu-client-secret-do-app

# --- Credenciais do Telegram ---
TELEGRAM_TOKEN=seu_token_do_bot
TELEGRAM_CHAT_ID=seu_chat_id
```

---

## ▶️ Como Rodar

### Opção 1: Modo Oculto 24/7 (Recomendado)
Para que o bot rode invisível em segundo plano sem abrir nenhuma "tela preta" que pode ser fechada por acidente:
- Dê um **clique duplo** no arquivo `RODAR_OCULTO.vbs`. 
- *(Dica de Ouro: Copie um atalho desse arquivo e cole na pasta `shell:startup` do Windows para o robô iniciar automaticamente quando o PC ligar).*

### Opção 2: Modo Terminal (Com visualização)
Caso precise investigar algum erro interno, ou para rodar na primeira vez:
```bash
python monitor_fabric.py
```
*(Ou apenas dê um clique duplo simples em `INICIAR_MONITOR.bat`)*

---

## 📦 Estrutura dos Arquivos Principais

- `monitor_fabric.py`: **[PRINCIPAL]** Script de monitoramento em Python contendo inteligência de resiliência.
- `RODAR_OCULTO.vbs`: Script que inicia o `monitor_fabric.py` totalmente em background (invisível de imediato).
- `INICIAR_MONITOR.bat`: Atalho para abrir a execução com a visualização clássica no prompt de comando.
- `monitor_state.json`: Arquivo que armazena cache (gerado automaticamente) para monitorar quais falhas já formam apitadas e evitas envios duplicados.
- `.env`: Configurações de chaves secretas e tokens (NUNCA envie para o GitHub).
- `requirements.txt`: Dependências essenciais da biblioteca Python.
