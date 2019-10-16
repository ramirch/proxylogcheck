import smtplib
from email.message import EmailMessage 

email = EmailMessage()
email["from"] = "ramirez_c99@hotmail.com"
email["to"] = "ramirez_c99@hotmail.com"
email["subject"] = "This is an email sent from Python"
email.set_content("I am a Python Developer.")

with smtplib.SMTP(host='smtp-mail.outlook.com', port='587') as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("ramirez_c99@hotmail.com", "")
    smtp.send_message(email)
    
