import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

from database import SessionLocal
from models import EmailHistory

load_dotenv()


class EmailService:

    def send_email(self, to_email, subject, message):

        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        server.login(sender_email, sender_password)

        server.sendmail(
            sender_email,
            to_email,
            msg.as_string()
        )

        server.quit()

        db = SessionLocal()

        email = EmailHistory(
            recipient=to_email,
            subject=subject,
            message=message
        )

        db.add(email)
        db.commit()
        db.close()

        return {
            "message": "Email sent successfully"
        }