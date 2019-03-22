import smtplib
import tldextract
from email.mime.text import MIMEText


def send_email(
    sender,
    pwd,
    recipients=[pyarmyknife.author_email],
    subject='Email from Python',
    body='',
    smtp='smtp.gmail.com:465',
):
    """Sends a text-only email to recipients; body can be str or filepath."""
    recipients = recipients if isinstance(recipients, list) else [recipients]
    body = open(body, 'rb').read() if path.isfile(body) else body
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'DdL <{}>'.format(sender)
    msg['To'] = ', '.join(recipients)
    smtpObj = smtplib.SMTP_SSL(smtp)
    smtpObj.ehlo()
    smtpObj.login(sender, pwd)
    failures = smtpObj.sendmail(sender, recipients, msg.as_string())
    smtpObj.close()
    return failures


def extract_domain(domain):
    domain = domain.replace('\xa0', ' ').strip(' ')
    return tldextract.extract(domain).fqdn.lower()


def extract_registered_domain(domain):
    domain = domain.replace('\xa0', ' ').strip(' ')
    return tldextract.extract(domain).registered_domain.lower()
