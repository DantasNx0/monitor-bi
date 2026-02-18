import requests
import os
import json
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações e Credenciais
TENANT_ID = os.getenv("TENANT_ID", "").strip()
CLIENT_ID = os.getenv("CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "").strip()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# Arquivo para salvar o estado (últimas falhas notificadas)
STATE_FILE = "monitor_state.json"
# Intervalo de verificação em segundos (10 minutos)
CHECK_INTERVAL = 600

def get_access_token():
    """Obtém o token de acesso via Service Principal (Client Credentials Flow)."""
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
        print("❌ ERRO: Credenciais (TENANT_ID, CLIENT_ID, CLIENT_SECRET) não encontradas no .env")
        return None

    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    body = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }
    
    try:
        response = requests.post(url, data=body)
        response.raise_for_status()
        return response.json().get('access_token')
    except Exception as e:
        print(f"❌ Falha na autenticação: {e}")
        if response.content:
            print(f"Detalhes: {response.text}")
        return None

def send_telegram_message(message):
    """Envia notificação para o Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram não configurado. Mensagem não enviada.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠️ Erro ao enviar Telegram: {e}")

def load_state():
    """Carrega o estado das últimas falhas notificadas."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    """Salva o estado atual."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"⚠️ Erro ao salvar estado: {e}")

def check_workspaces():
    """Função principal que varre workspaces e verifica datasets."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Iniciando verificação...")
    
    token = get_access_token()
    if not token:
        return

    headers = {'Authorization': f'Bearer {token}'}
    state = load_state()
    features_found = 0
    failures_found = 0

    try:
        # 1. Listar Workspaces (Groups)
        print("🔍 Listando Workspaces...")
        groups_url = "https://api.powerbi.com/v1.0/myorg/groups"
        resp = requests.get(groups_url, headers=headers)
        
        if resp.status_code != 200:
            print(f"❌ Erro ao listar Workspaces: {resp.status_code} - {resp.text}")
            return

        groups = resp.json().get('value', [])
        print(f"📂 Encontrados {len(groups)} Workspaces acessíveis.")

        for group in groups:
            group_id = group['id']
            group_name = group['name']
            
            # 2. Listar Datasets do Workspace
            ds_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets"
            ds_resp = requests.get(ds_url, headers=headers)
            
            if ds_resp.status_code != 200:
                print(f"⚠️ Erro ao ler datasets do workspace '{group_name}'")
                continue

            datasets = ds_resp.json().get('value', [])
            
            for ds in datasets:
                ds_id = ds['id']
                ds_name = ds['name']
                features_found += 1
                
                # 3. Pegar histórico de Refresh (Apenas o último)
                ref_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{ds_id}/refreshes?$top=1"
                ref_resp = requests.get(ref_url, headers=headers)
                
                if ref_resp.status_code == 200:
                    history = ref_resp.json().get('value', [])
                    if history:
                        last_run = history[0]
                        status = last_run.get('status')
                        
                        if status == 'Failed':
                            failures_found += 1
                            request_id = last_run.get('requestId')
                            end_time_str = last_run.get('endTime', '')
                            
                            # Formatar data para PT-BR se possível
                            try:
                                dt = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
                                # Converter para Horário de Brasília (UTC-3)
                                brt_tz = timezone(timedelta(hours=-3))
                                dt_br = dt.astimezone(brt_tz)
                                formatted_time = dt_br.strftime("%d/%m/%Y %H:%M:%S")
                            except Exception as e:
                                # Fallback para string original em caso de erro na conversão
                                print(f"⚠️ Erro ao converter data: {e}")
                                formatted_time = end_time_str

                            # Verificar se já notificamos este erro específico
                            last_notified_req_id = state.get(ds_id, {}).get('last_failed_request_id')
                            
                            if last_notified_req_id != request_id:
                                # Notificar!
                                error_json = last_run.get('serviceExceptionJson', '')
                                error_msg = "Erro desconhecido"
                                if error_json:
                                    # Tentar extrair mensagem limpa do JSON de erro se der
                                    error_msg = error_json[:300] # Limitar tamanho
                                
                                msg = (
                                    f"🚨 FALHA NA ATUALIZAÇÃO\n\n"
                                    f"🕒 Data: {formatted_time}\n"
                                    f"📂 Workspace: {group_name}\n"
                                    f"📊 Dataset: {ds_name}\n\n"
                                    f"❌ Erro: {error_msg}\n\n"
                                    f"[Monitor Python]"
                                )
                                print(f"🚨 Nova falha detectada em '{ds_name}'. Enviando alerta...")
                                send_telegram_message(msg)
                                
                                # Atualizar estado
                                state[ds_id] = {
                                    'last_failed_request_id': request_id,
                                    'dataset_name': ds_name,
                                    'workspace_name': group_name,
                                    'fail_time': formatted_time
                                }
                            else:
                                # Já notificado, ignora
                                pass

        print(f"✅ Ciclo concluído. {features_found} datasets verificados. {failures_found} falhas encontradas (sendo novas ou já conhecidas).")
        save_state(state)

    except Exception as e:
        print(f"❌ Erro crítico no loop: {e}")
        send_telegram_message(f"⚠️ Erro no script de monitoramento: {e}")

if __name__ == "__main__":
    print("🚀 Monitor de Power BI via API iniciado!")
    send_telegram_message("🚀 Monitor de Power BI iniciado! Vigiando os Workspaces.")
    
    while True:
        check_workspaces()
        print(f"💤 Aguardando {CHECK_INTERVAL/60} minutos...")
        time.sleep(CHECK_INTERVAL)
