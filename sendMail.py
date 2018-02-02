import mimetypes
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import listdir
from os.path import isfile, join

password = os.environ['password']
me = os.environ['from_mail']
you = os.environ['to_mail']

dir_path = 'attachments'
files = [file for file in listdir(dir_path) if isfile(join(dir_path, file))]

def attach_pdfs(message, files):
	for file in files:
		file_path='attachments2/'+file
		ctype, encoding = mimetypes.guess_type(file_path)
		if ctype is None or encoding is not None:
			ctype = dctype
		maintype, subtype = ctype.split('/', 1)
		with open(file_path, 'rb') as f:
			part = MIMEBase(maintype, subtype)
			part.set_payload(f.read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
			print os.path.basename(file_path)
			message.attach(part)


msg = MIMEMultipart('alternative')
msg['Subject'] = "SUBJECT"
msg['From'] = me
msg['To'] = you

html = '<html><body><p>SOME MESSAGE</p></body></html>'
part2 = MIMEText(html, 'html')
msg.attach(part2)
attach_pdfs(msg,files)

s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, password)

s.sendmail(me, you, msg.as_string())
s.quit()