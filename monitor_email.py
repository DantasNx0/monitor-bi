import imaplib
import email
import time
import requests
import os
from dotenv import load_dotenv
from email.header import decode_header
import threading

# Carrega variáveis de ambiente
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_SUBJECT_FILTER = os.getenv("EMAIL_SUBJECT_FILTER", "Erro no BI:")

def send_telegram_message(message):
    """Envia uma mensagem para o Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Erro: Credenciais do Telegram não configuradas no arquivo .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Mensagem enviada para o Telegram: {message}")
    except Exception as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")

def get_email_subject(msg):
    """Decodifica o assunto do email."""
    try:
        decoded_header = decode_header(msg["Subject"])[0]
        subject, encoding = decoded_header
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        return subject
    except Exception as e:
        return f"(Erro ao ler assunto: {e})"

def get_email_body(msg):
    """Extrai o corpo do email."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    return part.get_payload(decode=True).decode()
                except:
                    pass
    else:
        try:
            return msg.get_payload(decode=True).decode()
        except:
            pass
    return "Não foi possível ler o corpo do email."

def check_emails():
    """Conecta ao IMAP e verifica novos emails."""
    if not EMAIL_USER or not EMAIL_PASS or not IMAP_SERVER:
        print("Erro: Credenciais de Email não configuradas no arquivo .env")
        return

    try:
        # Conexão com SSL
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        
        print("Conectado e monitorando emails... (Pressione Ctrl+C para parar)")
        
        # Obtém o UID do último email existente para ignorar emails antigos
        mail.select("inbox")
        result, data = mail.uid('search', None, "ALL")
        if result == 'OK' and data[0]:
            last_seen_uid = int(data[0].split()[-1])
            print(f"Monitor iniciado. Ignorando emails com UID <= {last_seen_uid}")
        else:
            last_seen_uid = 0
            print("Caixa de entrada vazia ou erro ao buscar UIDs.")

        while True:
            try:
                # Busca emails com UID maior que o último visto
                status, messages = mail.uid('search', None, f'(UID {last_seen_uid + 1}:*)')
                
                if status == "OK" and messages[0]:
                    email_uids = messages[0].split()
                    
                    for email_uid in email_uids:
                        uid_int = int(email_uid)
                        if uid_int <= last_seen_uid:
                            continue
                            
                        # Atualiza o último UID visto
                        last_seen_uid = uid_int
                        
                        # Busca o cabeçalho do email
                        status, msg_data = mail.uid('fetch', email_uid, "(RFC822)")
                        
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                subject = get_email_subject(msg)
                                sender = msg.get("From")
                                body = get_email_body(msg)
                                
                                print(f"Novo email detectado (UID {uid_int}): {subject} de {sender}")
                                
                                if EMAIL_SUBJECT_FILTER.lower() in subject.lower():
                                    print("🚨 EMAIL DE ERRO ENCONTRADO!")
                                    # Limita o tamanho do corpo para não exceder limites do Telegram
                                    body_preview = body[:3000] + "..." if len(body) > 3000 else body
                                    send_telegram_message(f"🚨 ALERTA DE ERRO POWER BI\n\nAssunto: {subject}\nRemetente: {sender}\n\nDetalhes:\n{body_preview}")
                
                # Aguarda 60 segundos antes de verificar novamente
                time.sleep(60)
                
                # Envia comando NOOP para manter a conexão ativa
                mail.noop()
                
            except Exception as e:
                print(f"Erro durante o loop de verificação: {e}")
                print("Tentando reconectar em 60 segundos...")
                time.sleep(60)
                # Tenta reconectar
                try:
                    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
                    mail.login(EMAIL_USER, EMAIL_PASS)
                    mail.select("inbox")
                except:
                    pass

    except Exception as e:
        print(f"Erro fatal na conexão: {e}")

if __name__ == "__main__":
    # Testa o envio de mensagem ao iniciar
    send_telegram_message("🤖 Monitor de Power BI Iniciado! Vou te avisar se chegar email de erro.")
    check_emails()
