import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def enviar_email_vaga(cliente: str, cargo: str):
    try:
        host = "smtp.gmail.com"
        gmail_user = st.secrets["gmail"]["user"]
        app_password = st.secrets["gmail"]["app_password"]

        mensagem = f"""
        <p>Informamos que a vaga para o cargo de <b>{cargo}</b> no cliente <b>{cliente}</b> foi cadastrada.</p>
        <p>Atenciosamente,<br>Parma Consultoria</p>
        """
        msg = MIMEText(mensagem, "html", "utf-8")
        msg["Subject"] = Header(f"Nova Vaga Cadastrada - {cargo} ({cliente})", "utf-8")
        msg["From"] = formataddr(("Parma Consultoria", gmail_user))
        destinatarios = ["rogerio@parmaconsultoria.com.br", "atendimento@parmaconsultoria.com.br"]
        msg["To"] = ", ".join(destinatarios)

        with smtplib.SMTP_SSL(host, 465, timeout=30) as server:
            server.login(gmail_user, app_password)
            server.sendmail(gmail_user, destinatarios, msg.as_string())

        st.success(f"📧 E-mail enviado: {', '.join(destinatarios)}")
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
