# price checker
# it sends email to $toaddr
# if price on shoes of your dream was decreased to $critical_price

import requests
from bs4 import BeautifulSoup
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


url = 'https://intertop.ua/catalog/muzhskaya_obuv/tommy-hilfiger_680/'
fromaddr = "from-email@gmail.com"
toaddr = "to-email@gmail.com"
critical_price = 3900


def check_price():
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    samples = soup.find_all("span", 'price-contain')
    shoes_price = float(samples[0].text.strip())
    print(shoes_price)
    return shoes_price


def send_email(body):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your shoes are not so expensive now!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "y0ur-p@55w0rd")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print("Successfully sent email.\n")
    except:
        print("Error: unable to send email.\n")


def main():
    shoes_price = check_price()
    if shoes_price < critical_price:
        body = "Time to buy. Price is bellow {}. Visit {}".format(critical_price, url)
        send_email(body)
    else:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('{} - Price is {} UAH and still high.\n'.format(current_date, shoes_price))


if __name__ == "__main__":
    main()
