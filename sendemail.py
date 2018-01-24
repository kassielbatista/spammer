#!/usr/bin/env python

import smtplib
import sys
import tempfile
from subprocess import call
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

SMTP_SERVER = config("SMTP_SERVER")
SMTP_PORT = config("SMTP_PORT")
EMAIL_ADDRESS = config("EMAIL_ADDRESS")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")


def read_message():
    """
    Opens an editor to receive a text or html message to be sent as the message body of the email.

    :return:
    """
    editor = config("EDITOR", default="vim")

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        call([editor, tf.name])

        tf.seek(0)
        return tf.read()


def prepare_message():
    """
    Prepares the message to be sent.

    :return:
    """
    msg_to_send = MIMEMultipart('alternative')
    msg_to_send['Subject'] = raw_input("Enter the subject of the email: ")
    msg_to_send['From'] = EMAIL_ADDRESS

    msg_to_send.attach(MIMEText(read_message(), 'html'))

    return msg_to_send


def smtp_connect():
    """
    This function initializes and greets the smtp server.
    It logs in using the provided credentials and returns the smtp server object as a result.
    :return:
    """

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    return server


def send_email(email, prepared_message):
    """
    Send the email using the previous prepared message received as a parameter.

    :param email:
    :param prepared_message:
    :return:
    """

    server = smtp_connect()
    server.sendmail(prepared_message['From'], email, prepared_message.as_string())
    server.close()


if __name__ == "__main__":
    print("""
        Welcome to Mail Spammer.
        
        This simples script reads a file with a list of emails that you will input next.
        
        Then it will open a Vim text editor so you can enter the message that you want people in the list to receive.
        
        After that, you just need to wait until it finish.
        
        Enjoy. 
    """)

    argfile = raw_input("Enter the path to the emails list file:")
    argfile = open(argfile, 'r')

    prepared_message = prepare_message()

    for email in argfile.readlines():
        try:
            print("Sending to: " + email)
            send_email(email, prepared_message)
            print("Success!")
        except:
            e = sys.exc_info()[0]
            print("Error: It was not possible to send your email to: " + email)
            print("Message: " + e),


