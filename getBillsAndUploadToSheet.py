# # !/bin/python
import imaplib
import os
from bs4 import BeautifulSoup
import email
import re
import textract
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds',
		'https://www.googleapis.com/auth/drive']

# provide connectionWithG-Drive key after creating project in google drive
g_drive_key = os.environ['connectionKey']

credentials = ServiceAccountCredentials.from_json_keyfile_name(g_drive_key, scope)
gc = gspread.authorize(credentials)


wks = gc.open("expense-reimbursement-Dec").get_worksheet(0)


mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)

email_id = os.environ['email']
password = os.environ['password']
label = os.environ['label']	#label in gmail (ex:= olabills)
detach_dir = '.'
dir_path = 'attachments5'

if dir_path not in os.listdir(detach_dir):
	os.mkdir(dir_path)

mail.login(email, password)
mail.list()
mail.select(label)
#SINCE 01-Jan-2018 pattern used to search mail from 1 jan in given label
result, data = mail.search(None, '(SINCE 01-Jan-2018)')
ids = data[0]
id_list = ids.split()
count = 0

list = []

#coverts given pdf file as text file
def convert_to_text(pdf_file):
	text = textract.process(pdf_file)
	return text.strip()

# create a bill object with bill date and price from a given pdf file
def create_a_bill(file_path):
	text = convert_to_text(file_path)
	content = filter(None,text.split("\n"))
	# For getting price from pdf file
	if 'Invoice Serial Id' not in content[1]:
		price_from = content[1]
	else:
		# For getting price from mail content not pdf file
		price_from = content[2]
	price = (price_from.strip())[-2:]

	# Remove unicode from price
	if(price == '\xb90'):
		price = '0'
	print(price, date)
	return {'date':content[0], 'price':price}


for latest_email_id in id_list:
	try:
		result, data = mail.fetch(latest_email_id, "(RFC822)") 
		count = count + 1
		print count
	except Exception as e:
		print e

	# Get raw data of email content
	raw_email = data[0][1]

	formatted_mail = email.message_from_string(raw_email)
	# Getting bill date from mail content
	date = formatted_mail['Date'].split(",")[1].strip()
	bill_date = " ".join(date.split(" ")[:3])

	cleantext = BeautifulSoup(str(formatted_mail), "lxml").text
	# used to get OSN (for ola share) or CRN number of ola ride
	regex = r'(OSN[0-9].*|CRN[0-9].*)'
	patttern = re.compile(regex)
	cdn = re.findall(patttern, cleantext)[0]

	# Ola share rides often have image attached with mail instead of pdf file
	# Getting price for ola share ride
	if("OSN" in cdn):
		a = cleantext.split("Paid by Cash mone")[1]
		price = a.split()[1]
		print(price, bill_date)
		list.append({'date':bill_date, 'price':str(price)})

	else:
		for part in formatted_mail.walk():
			fileName = part.get_filename()
		# Reading from a pdf file for CRN and creating bill for it
			if not(fileName is None):
				filePath = os.path.join(detach_dir, dir_path, fileName)
				if not os.path.isfile(filePath):
					fp = open(filePath, 'wb')
					fp.write(part.get_payload(decode=True))
					fp.close()
				
				bill = create_a_bill(filePath)
				list.append(bill)


# Writing bill with price in ola rides sheet
def update_into_google_sheet(bills):
	for j, bill in enumerate(bills, start=16):
		wks.update_cell(j, 1, bill['date'])
		wks.update_cell(j, 2, 'Travel expenses')
		wks.update_cell(j, 5, bill['price'])
		print('updated google sheet successfully', bill)
	return 'successed...'


update_into_google_sheet(list)
