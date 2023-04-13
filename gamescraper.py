import os
from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from dotenv import load_dotenv


load_dotenv()


def send_email():

    source = requests.get("https://sportsgamestoday.com/").text

    soup = BeautifulSoup(source, "lxml")

    games_table = soup.find("table")

    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    sender_password = os.getenv("SENDER_PASS")
    # message = games_table
    html = games_table

    subject = "Check out today's games!"

    email_message = MIMEMultipart()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = subject
    email_message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, email_message.as_string())


send_email()
# schedule.every().day.at("09:15").do(send_email)

# while True:
#     schedule.run_pending()
#     tm.sleep(1)
