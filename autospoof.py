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
p.add_argument('-t', 
               '--to', 
               type=str, 
               help='to address', 
               required='True')
p.add_argument('-f', 
              '--From', 
              type=str, 
              help='from address', 
              required='True')
p.add_argument('-j', 
              '--subject', 
              type=str, 
              help='email subject', 
              required='True')
p.add_argument('-F', 
              '--filename', 
              type=str, 
              help='file attachment', 
              required='False')
args = p.parse_args()

class mysmtp:
   def __init__(self, server, port, toEmail, fromEmail, subject, filename):
       self.server = server 
       self.port = port
       self.toEmail = toEmail
       self.fromEmail = fromEmail
       self.subject = subject
       self.filename = filename

   def send_message(self):
        
       msg = MIMEMultipart('alternative')
       msg['From'] = self.fromEmail
       msg['To'] = self.toEmail
       msg['Subject'] = self.subject
       body = 'sent w/ smtplib and email.mime py libs'
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


q = mysmtp(args.server, args.port, args.to, args.From, args.subject, args.filename)
q.send_message()
