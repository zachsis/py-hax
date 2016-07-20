import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

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
              help='display from to fool mail clients. ' +
              'useful if you cant spoof your MAILFROM', 
              required='True')
p.add_argument('-d', 
              '--displayemail', 
              type=str, 
              help='display from to fool mail clients. ' +
              'useful if you cant spoof your MAILFROM', 
              required='False')
p.add_argument('-x', 
              '--xsender, 
              type=str, 
              help='rtfm or rtfrfc' +
              'useful if you cant spoof your MAILFROM', 
              required='False')
p.add_argument('-j', 
              '--subject', 
              type=str, 
              help='email subject', 
              required='True')
p.add_argument('-f', 
              '--filename', 
              type=str, 
              help='file attachment')
p.add_argument('-p', 
              '--replyto', 
              type=str, 
              help='reply to header. rtfrfc')
p.add_argument('-n', 
              '--returnpath', 
              type=str, 
              help='reply to header. rtfrfc')
args = p.parse_args()

class mysmtp:
   def __init__(self, server, port, rcptto, mailfrom, subject, 
                displayname, displayemail, xsender, replyto, returnpath):
       self.server = server 
       self.port = port
       self.rcptto = rcptto
       self.mailfrom = mailfrom
       self.subject = subject
       self.displayname = ''
       self.displayemail = ''
       self.replyto = ''
       self.xsender = ''
       self.filename = ''
       self.returnpath = ''

   def send_message(self):
        
       msg = MIMEMultipart('alternative')
       msg['From'] = self.mailfrom
       msg['To'] = self.rcptto
       msg['Subject'] = self.subject
       
       if self.displayname:
         d = "{} \"<{}>\"\r\n".format(self.displayname, self.displayemail)
       else:
         d = ''
       if self.xsender:
         x = "X-Sender: {} \"<{}>\"\r\n".format(self.displayname, self.displayemail)
       else:
         x = ''
       if self.replyto:
         rto = "Reply-To: {} \"{}\"\r\n".format(self.displayname, self.replyto)
       else:
         rto = ''
       if self.returnpath:
         rpat = "Return-Path: {} \"{}\"\r\n".format(self.displayname, self.returnpath)
       else:
         rpat = ''
       body = "{}{}{}{}sent w/ smtplib and email.mime py libs".format(d,x,rto,rpat)
       content = MIMEText(body, 'plain')
       msg.attach(content)
       if self.filename:
           f = file(self.filename)
           attachment = MIMEText(f.read())
           attachment.add_header('Content-Disposition',
                                 'attachment', 
                                 filename=self.filename)
           msg.attach(attachment)
           print f
       try: 
           print '[+] attempting to send message'
           s = smtplib.SMTP(self.server, self.port)
           s.sendmail(self.fromEmail, self.toEmail, msg.as_string())
           print '[$] successfully sent through {}:{}'.format(self.server,
                                                              self.port)
       except socket.error as e:
           print '[!] could not connect'


q = mysmtp(args.server, args.port, args.to, args.From, args.subject)
if args.filename:
    q.filename = args.filename
q.send_message()
