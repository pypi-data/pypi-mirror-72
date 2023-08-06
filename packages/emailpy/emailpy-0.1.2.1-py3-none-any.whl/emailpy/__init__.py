__version__ = '0.1.2.1'
__author__ = 'Sandra Mattar'
__email__ = 'sandrawmattar@gmail.com'
__url__ = 'https://pypi.org/project/emailpy'

"""
A Python interface for sending, reading, and deleting emails

Functions:
    readmail - read an email
    sendmail - send an email
    sendmailobj - send an EmailMessage object with specs
    forward - forward an EmailMessage object with specs

Usage:
    >>> import emailpy
    >>> sent = emailpy.sendmail("fromemail@gmail.com", "fromemail_password",
                    toemails = ["toemail1@gmail.com", "toemail2@gmail.com")
                    subject = 'Subject', body = 'Body',
                    attachments = ['file.txt', 'picture.png'])
    >>> # send an email from
    >>> # "fromemail@gmail.com" and password "fromemail_password" to
    >>> # "toemail1@gmail.com" and "toemail2@gmail.com" with subject
    >>> # "Subject" and body "Body" and retreive the message into the variable
    >>> # "sent". 
    >>> data = emailpy.readmail("toemail1@gmail.com", "toemail1_password") # read
    >>> # email "toemail1@gmail.com" with password "toemail1_password"
    >>> data = data[0] # get first email from EmailMessageList object
    >>> data.body # "Body"
    >>> data.subject # "Subject"
    >>> data.html # "Body"
    >>> data.sender # "fromemail@gmail.com"
    >>> data.recvers # ["toemail1@gmail.com", "toemail2@gmail.com"]
    >>> data.show() # <showing in selenium chrome>
    >>> data.attachments # <EmailAttachment Object filenames=["file.txt",
    >>> # "picture.png"]>
    >>> data.attachments.download() # save attached files to computer
    >>> data.attachments.show() # show attached files
    >>> # WARNING: when using data.attachments.show(), you must first call
    >>> # data.attachments.download()
    >>> data.is_attachment # True
    >>> data.delete() # delete email
    >>> emailpy.sendmailobj(sent, attachments = ['file2.txt']) # send the sent
    >>> # variable as an email, but replacing the attachments list with
    >>> # ['file2.txt'].
    >>> emailpy.forward(data, 'forwardtome@yahoo.com', body = 'hi') # forward
    >>> # the read email to "forwardtome@yahoo.com", but replacing the body
    >>> # with "hi". NOTE that this only works on read emails. So, you cannot
    >>> # use the emailpy.forward() method on sent or forwarded emails. 
"""

import sys

if not ((sys.version_info[0] == 3) and (sys.version_info[1] >= 8)):
    class VersionError(BaseException):
        pass

    raise VersionError('package "emails" requires python 3.8 or above. ')

from .read import readmail
from .send import sendmail, sendmailobj, forward
from .util import EmailSender, EmailReader
from .gethostport import gethostport
from smtplib import SMTP as _Login
_LoginMode = 'smtp'

def login(email, pwd):
    host, port = gethostport(email, _LoginMode)
    try:
        s = _Login(host, port)
        s.ehlo()
        s.starttls()
        s.login(email, pwd)
    except:
        return False
    else:
        return True
