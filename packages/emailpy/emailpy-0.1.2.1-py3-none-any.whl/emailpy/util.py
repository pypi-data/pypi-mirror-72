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
