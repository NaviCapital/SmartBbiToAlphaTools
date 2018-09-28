import traceback
import datetime
import os

def log(fullpath, text):
    log = "################\n"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log += f"{now}\n" + text + "\n"
    file = open(fullpath, "a")
    file.write(log)

from smtplib import SMTP
from email.mime.text import MIMEText

def send_email(subject, body, toaddr=os.getenv("SMTP_TO")):
    msg = MIMEText(body, 'plain')
    msg['To'] = toaddr
    msg['Subject'] = subject

    server = SMTP(os.getenv("SMTP_SERVER"), 587)
    server.ehlo()
    server.starttls()
    server.login(os.getenv("SMTP_FROM"), os.getenv("SMTP_PASS"))
    server.sendmail(os.getenv("SMTP_FROM"), toaddr, msg.as_string())
    server.quit()
