import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse


### Need to add a Sender header option

p = argparse.ArgumentParser()
p.add_argument('-s',
               '--server',
               type=str,
               help='smtp server',
               required='True')
p.add_argument('-p',
               '--port',
               type=int,
               help='smtp server port',
               required='True')
p.add_argument('-r',
               '--rcptto',
               type=str,
               help='to address',
               required='True')
p.add_argument('-m',
               '--mailfrom',
               type=str,
               help='MAIL FROM email headers. ' +
                    'please note this email may need to be set ' +
                    'as a valid domain you are sending from to ' +
                    'bypass spf checks',
               required='True')
p.add_argument('-d',
               '--displayname',
               type=str,
               help='display name to fool mail clients. ' +
                    'useful if you cant spoof your MAILFROM',
               required='True')
p.add_argument('-l',
               '--displayemail',
               type=str,
               help='display from email to fool mail clients. ' +
                    'useful if you cant spoof your MAILFROM'
               )
p.add_argument('-j',
               '--subject',
               type=str,
               help='email subject',
               required='True')
p.add_argument('-f',
               '--filename',
               type=str,
               help='file attachment')
p.add_argument('-P',
               '--replyto',
               type=str,
               help='reply to header. rtfrfc')
p.add_argument('-b',
               '--bodyfile',
               type=str,
               help='text file to import as the message body.')
p.add_argument('-S',
               '--sender',
               type=str,
               help='Sender header, useful for spoofing. rtfrfc')
args = p.parse_args()


class MySmtp:
    def __init__(self, server, port, rcptto, mailfrom, subject,
                 displayname='', displayemail='',
                 replyto='', filename='', bodyfile='', sender=''):
        self.server = server
        self.port = port
        self.rcptto = rcptto
        self.mailfrom = mailfrom
        self.subject = subject
        self.displayname = displayname
        self.displayemail = displayemail
        self.replyto = replyto
        self.filename = filename
        self.bodyfile = bodyfile
        self.sender = sender

    def send_message(self):
        msg = MIMEMultipart('alternative')
        msg['To'] = self.rcptto
        msg['Subject'] = self.subject
        if self.displayname:
            msg['From'] = "{} <{}>".format(self.displayname, self.displayemail)
        else:
            msg['From'] = "{}".format(self.mailfrom)
        if self.replyto:
            rto = "{}".format(self.replyto)
            msg.add_header('Reply-To', rto)
        if self.sender:
            sen = "{}".format(self.sender)
            msg.add_header('Sender', sen)
        if self.bodyfile:
            f = file(self.bodyfile)
            content = MIMEText(f.read(), 'plain')
#            content = MIMEText(self.body, 'plain')
            msg.attach(content)
        if self.filename:
            f = file(self.filename)
            attachment = MIMEText(f.read())
            attachment.add_header('Content-Disposition',
                                  'attachment',
                                  filename=self.filename)
            msg.attach(attachment)
        try:
            print '[+] attempting to send message'
            s = smtplib.SMTP(self.server, self.port)
            s.sendmail(self.mailfrom, self.rcptto, msg.as_string())
            print '[$] successfully sent through {}:{}'.format(self.server, self.port)
        except socket.error as e:
            print '[!] could not connect'


def main():
    q = MySmtp(args.server,
               args.port,
               args.rcptto,
               args.mailfrom,
               args.subject,
               args.displayname,
               args.displayemail,
               args.replyto,
               args.filename,
               args.bodyfile,
               args.sender)

    q.send_message()

main()
