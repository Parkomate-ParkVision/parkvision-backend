from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading
from backend.celery import app
import os
import dotenv

dotenv.load_dotenv()


class SendEmailThread(threading.Thread):
    def __init__(self, receiver, subject, message, cc=""):
        self.email = os.environ.get('EMAIL')
        self.password = os.environ.get('EMAIL_PASSWORD')
        self.receiver = receiver
        self.subject = subject
        self.message = message
        self.cc = cc
        threading.Thread.__init__(self)

    def run(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(0)
            server.ehlo()
            server.starttls()
            server.login(self.email, self.password)

            body = MIMEMultipart("alternative")
            body["Subject"] = self.subject
            body["From"] = self.email
            body["To"] = self.receiver
            body.attach(MIMEText(self.message, 'html'))
            if self.cc != "":
                body['Cc'] = self.cc
                rcpt = [self.receiver] + self.cc.split(',')
            else:
                rcpt = [self.receiver]
            server.sendmail(self.email, rcpt, body.as_string())
            return True
        except Exception as e:
            print(e)
            return False


@app.task(bind=True)
def send_email(receiver, subject, message, cc='', *args, **kwargs):
    SendEmailThread(receiver=receiver, subject=subject,
                    message=message, cc=cc).start()
