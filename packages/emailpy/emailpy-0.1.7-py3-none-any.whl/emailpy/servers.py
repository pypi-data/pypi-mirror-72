from .gethostport import gethostport
import smtplib
import imaplib

def getserver(email, mode):
    if mode == 'smtp':
        return smtplib.SMTP(*gethostport(email, mode))
    elif mode == 'imap':
        return imaplib.IMAP4_SSL(*gethostport(email, mode))
