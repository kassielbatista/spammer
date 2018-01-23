#!/usr/bin/env python

import smtplib
import sys


def smtp_connect():
    """
    This function initializes and greets the smtp server.
    It logs in using the provided credentials and returns the smtp server object as a result.
    :return:
    """

    smtpserver = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(GMAIL_EMAIL, GMAIL_PASSWORD)

    return smtpserver


def send_thank_you_mail(email):
    
    to_email = email
    from_email = GMAIL_EMAIL
    subj = "Thanks for being an active commenter"

    header = "To:%s\nFrom:%s\nSubject:%s \n" % (to_email, from_email, subj)

    msg_body = """
    Hi %s,
    
    Thank you very much for your repeated comments on our service.
    
    The interaction is much appreciated.
    
    Thank you.""" % email

    content = header + "\n" + msg_body

    smtpserver = smtp_connect()
    smtpserver.sendmail(from_email, to_email, content)
    smtpserver.close()


if __name__ == "__main__":

    for email in sys.stdin.readlines():
        send_thank_you_mail(email)