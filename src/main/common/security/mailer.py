import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from common.env import settings

def send_verify_email(to_email:str, verify_url:str):
    subject = "이메일 인증을 완료해주세요."
    html = f"""
    <html>
        <body>
            <p>안녕하세요! 아래 링크를 클릭하여 이메일 인증을 완료해주세요.</p>
            <p>{verify_url}</p>
            <p>감사합니다</p>
        </body>
    </html>
"""
    SMTP_USER = settings.profile_config.SMTP_USER
    msg = MIMEText(html, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Support", SMTP_USER))
    msg["To"] = to_email

    SMTP_HOST = settings.profile_config.SMTP_HOST
    SMTP_PORT = settings.profile_config.SMTP_PORT

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)
