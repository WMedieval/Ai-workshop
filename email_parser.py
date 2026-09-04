#!/usr/bin/env python3
"""
email_parser.py – BauMind AI Email Parser
Čita emailove preko IMAP-a i analizira ih pomoću ChatGPT-a.
"""

import imaplib
import email
from email.header import decode_header
import openai
import json
import os
from datetime import datetime

# ==================== KONFIGURACIJA ====================
# Ove podatke ćete uneti u config.json ili kao environment varijable
EMAIL_HOST = os.getenv("EMAIL_HOST", "imap.gmail.com")
EMAIL_USER = os.getenv("EMAIL_USER", "your_email@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "your_app_password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key")

openai.api_key = OPENAI_API_KEY

# ==================== FUNKCIJE ====================

def connect_to_email():
    """
    Povezivanje na email server preko IMAP-a.
    """
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("INBOX")
        return mail
    except Exception as e:
        print(f"❌ Greška pri povezivanju na email: {e}")
        return None

def fetch_unread_emails(mail, limit=10):
    """
    Preuzima nepročitane emailove.
    """
    try:
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            return []
        
        email_ids = messages[0].split()
        emails = []
        
        for e_id in email_ids[:limit]:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue
                
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Dekodiranje naslova i pošiljaoca
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode("utf-8", errors="ignore")
                
            from_ = decode_header(msg.get("From"))[0][0]
            if isinstance(from_, bytes):
                from_ = from_.decode("utf-8", errors="ignore")
                
            # Telo emaila
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if "attachment" not in content_disposition:
                        try:
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                except:
                    body = str(msg.get_payload())
            
            emails.append({
                "id": e_id.decode(),
                "from": from_,
                "subject": subject,
                "body": body[:1000],  # Ograđivanje radi performansi
                "date": msg.get("Date")
            })
            
        return emails
    except Exception as e:
        print(f"❌ Greška pri čitanju emailova: {e}")
        return []

def analyze_email_with_ai(email_content):
    """
    Šalje email ChatGPT-u na analizu.
    """
    try:
        prompt = f"""
        Analiziraj sledeći email i izvuci ključne informacije:
        
        Od: {email_content['from']}
        Naslov: {email_content['subject']}
        Telo: {email_content['body'][:500]}
        
        Odgovori u JSON formatu:
        {{
            "kategorija": "ponuda|reklamacija|upit|ostalo",
            "projekat": "ime projekta ili nepoznato",
            "iznos": broj ili null,
            "rok": "datum ili null",
            "hitnost": "visoka|srednja|niska",
            "preporuka": "kratka preporuka za akciju",
            "predlog_odgovora": "generisan odgovor"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ti si AI asistent za građevinske firme. Analiziraj emailove."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        # Čistimo JSON iz odgovora
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
        
    except Exception as e:
        print(f"❌ Greška pri AI analizi: {e}")
        return {
            "kategorija": "nepoznato",
            "projekat": "nepoznato",
            "iznos": None,
            "rok": None,
            "hitnost": "niska",
            "preporuka": "Pregledajte email ručno.",
            "predlog_odgovora": "Hvala na poruci. Odgovorićemo uskoro."
        }

def process_emails():
    """
    Glavna funkcija – čita emailove, analizira ih i vraća rezultate.
    """
    mail = connect_to_email()
    if not mail:
        return []
    
    emails = fetch_unread_emails(mail, limit=5)
    mail.close()
    mail.logout()
    
    results = []
    for email_data in emails:
        analysis = analyze_email_with_ai(email_data)
        results.append({
            "email": email_data,
            "analysis": analysis
        })
    
    return results

# ==================== POKRETANJE ====================
if __name__ == "__main__":
    print("📬 BauMind AI – Email Parser")
    print("=" * 40)
    
    results = process_emails()
    
    for i, result in enumerate(results):
        print(f"\n📧 Email #{i+1}")
        print(f"   Od: {result['email']['from']}")
        print(f"   Naslov: {result['email']['subject']}")
        print(f"   Kategorija: {result['analysis']['kategorija']}")
        print(f"   Projekat: {result['analysis']['projekat']}")
        print(f"   Iznos: {result['analysis']['iznos']}")
        print(f"   Hitnost: {result['analysis']['hitnost']}")
        print(f"   💡 Preporuka: {result['analysis']['preporuka']}")
        print(f"   ✉️ Predlog odgovora: {result['analysis']['predlog_odgovora'][:100]}...")
