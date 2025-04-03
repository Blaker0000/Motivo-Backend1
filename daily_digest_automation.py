# daily_digest_automation.py
import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email credentials
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")

# Fetch recent Q&A history from memory
def fetch_recent_digest():
    conn = sqlite3.connect("chatbot_memory.db")
    c = conn.cursor()
    c.execute("SELECT question, answer FROM memory ORDER BY id DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    digest = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in rows])
    return digest or "No recent Q&A data found."

# Send digest email
def send_digest_email():
    digest = fetch_recent_digest()
    msg = MIMEText(digest)
    msg['Subject'] = 'Daily AI Digest - Motivo Chatbot'
    msg['From'] = EMAIL_USER
    msg['To'] = ", ".join(EMAIL_RECIPIENTS)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.connect(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_RECIPIENTS, msg.as_string())
            print("✅ Digest email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_digest_email()
