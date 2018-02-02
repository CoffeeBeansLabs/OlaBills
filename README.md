# OlaBills
It is library to submit ola bills

# sendOlaInvoiceToMail
It is a js based library used to send invoice mail using ola invoice api.

## Requirements
 * nodejs
 * selenium webdriver
 * chrome webdriver
 
## How to run
```shell
node sendOlaInvoiceToMail.js
```

# getBillsAndUploadToSheet
It is a python based library to get bills from ola share and ola bills pdf and upload to google sheet.

## Requirements
* python2
python libraries:
* imaplib //To read mail from gmail
* bs4
* textract
* gspread  //google sheet library
* oauth2client.service_account //for authenticate account for google sheet

```shell
Enable "google as less secure" before running this library.
```
## How to run
```shell
python getBillsAndUploadToSheet.py
```

# sendMail
It is a python based library to get all downloaded pdf files and send them to provided mail id

## Requirements
* python2
python libraries:
* mimetypes
* encoders
* smtplib //for sending mail from browser
* email
* email.mime.base
* email.mime.multipart
* email.mime.text

## How to run
```shell
python sendMail.py
```

