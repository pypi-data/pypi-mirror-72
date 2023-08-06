from base64 import *
from .send import sendmail
from .read import readmail

class EmailSender:
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = b85encode(pwd.encode())

    def send(self, toemails, subject = '', body = '', html = None,
             attachments = None, nofileattach = None):
        return sendmail(self.email, b85decode(self.pwd).decode(),
                        toemails, subject, body, html,
                        attachments, nofileattach)

class EmailReader:
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = b85encode(pwd.encode())

    def read(self, foldername = 'INBOX'):
        return readmail(self.email, b85decode(self.pwd).decode(),
                        foldername)

class EmailManager:
    def __init__(self, email, pwd):
        self.sender = EmailSender(email, pwd)
        self.reader = EmailReader(email, pwd)

    def send(self, toemails, subject = '', body = '', html = None,
             attachments = None, nofileattach = None):
        return self.sender.send(toemails, subject, body, html,
                        attachments, nofileattach)

    def read(self, foldername = 'INBOX'):
        return self.reader.read(foldername)
