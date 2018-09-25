import traceback
import datetime
import os

def log_error(fullpath):
    error = "################\n"
    now = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    error += f"{now}\n" + traceback.format_exc() + "\n"
    file = open(fullpath, "a")
    file.write(error)
    print(error)


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
