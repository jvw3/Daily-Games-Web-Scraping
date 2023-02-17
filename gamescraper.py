import os
from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from dotenv import load_dotenv
import datetime
import pytz
import schedule
import time as tm


# dt = datetime.datetime.now(tz=pytz.timezone("US/Central"))


load_dotenv()


def send_email():

    source = requests.get("https://sportsgamestoday.com/").text

    soup = BeautifulSoup(source, "lxml")
    # print(soup.prettify())

    # title = soup.find("div", class_="gametitle").text

    games_table = soup.find("table")
    # print(games_table)

    # for game in games_table.find_all('tr'):

    #     full_game_schedule = game.text

    # if game.find('th'):
    #     section_title = soup.find('th', class_='gamematchuptitle')
    #     game_time_title = soup.find('th', class_='gametimetitle')
    #     section_channel = soup.find('th', class_='gamechanneltitle')
    #     print(section_title)

    #     print(game_time_title)
    #     print(section_channel)
    # else:
    #     game_title = soup.find('td', class_='gamematchup')
    #     game_time = soup.find('td', class_='gametime')
    #     channel_name = soup.find('td', class_='gamechannel')
    #     print(game_title)
    #     print(game_time)
    #     print(channel_name)

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


schedule.every().day.at("15:50").do(send_email)

while True:
    schedule.run_pending()
    tm.sleep(1)
