from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library

import smtplib
import tldextract
from email.mime.text import MIMEText

standard_library.install_aliases()


def send_email(
    sender,
    pwd,
    recipients,
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


def extract_domain(url, with_subdomain=False):
    """Extract domain from url, needs a proper domain/suffix.

    with_subdomain=True
        Return a Fully Qualified Domain Name with suffix.
    with_subdomain=False
        Return only the registered domain with suffix.
    """
    assert isinstance(url, str) and url, f'Input "{url}" is not accepted'
    url = url.replace('\xa0', ' ').strip(' \n')
    if with_subdomain:
        fqdn = tldextract.extract(url).fqdn.lower()
        return fqdn[4:] if fqdn.startswith('www.') else fqdn
    else:
        return tldextract.extract(url).registered_domain.lower()
