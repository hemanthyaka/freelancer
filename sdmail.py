import smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('yakahemanth3@gmail.com','mwni vwkg pbmi vrah')
    msg=EmailMessage()
    msg['From']='yakahemanth3@gmail.com'
    msg['To']=to
    msg['Subject']=subject
    msg.set_content(body)
    server.send_message(msg)
    server.quit()