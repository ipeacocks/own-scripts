from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup

import datetime
import time
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class CheckPrice:
    def __init__(self, url, fromaddr, toaddr, email_pass, price_limit):
        self.url = url
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.email_pass = email_pass
        self.price_limit = price_limit

    def get_html(self):
        # Getting rendered html page
        # s = Service(GeckoDriverManager().install())
        # driver = webdriver.Firefox(service=s)
        driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
        driver.get(self.url)
        time.sleep(1)
        html_source = driver.page_source
        driver.close()
        return html_source

    def parse_html(self, html_source):
        self.html_source = html_source
        # Parsing it for needed data
        soup = BeautifulSoup(self.html_source, "html.parser")
        samples = soup.select("div.product-details")
        watch_dic = {}

        # for item in samples:
        #     element = item.find_all('span')
        #     model = element[1].get_text().strip()
        #     # convert dolars to float
        #     price = float(element[2].get_text().strip()[1:])
        #     # print(f"{model} - {price}")
        #     watch_dic[model] = price

        element = samples[0].find_all("span")
        model = element[1].get_text().strip()
        # convert dolars to float
        price = float(element[2].get_text().strip()[1:])
        link = samples[0].find_all("a")[0].get("href")
        # print(f"{model} - {price} - {link}")
        # watch_dic[model] = price

        return model, price, link

    def send_email(self, body, smtp_address, port):
        self.body = body
        self.smtp_address = smtp_address
        self.port = port
        msg = MIMEMultipart()
        msg["From"] = self.fromaddr
        msg["To"] = self.toaddr
        msg["Subject"] = "There is good watch price for you!"
        msg.attach(MIMEText(self.body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_address, self.port)
            server.starttls()
            server.login(self.fromaddr, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.fromaddr, self.toaddr, text)
            server.quit()
            print("Successfully sent email.\n")
        except:
            print("Error: unable to send email.\n")


def main():
    BASIC_URL = "https://www.jomashop.com"
    SEARCH_URL = "/watches-for-men.html?manufacturer=Junghans&series=Max+Bill%7CMax+Bill+Mega&sort=price_asc%7Casc"
    PRICE_LIMIT = 395

    FROMADDR = os.environ["FROMADDR"]
    TOADDR = os.environ["TOADDR"]
    smtp_address = "smtp.gmail.com"
    port = 587

    # 6 hours is 21600 seconds
    delay = os.getenv("DELAY", 21600)

    while True:
        watch_price = CheckPrice(
            BASIC_URL + SEARCH_URL,
            FROMADDR,
            TOADDR,
            os.environ["EMAIL_PASS"],
            PRICE_LIMIT,
        )
        html_source = watch_price.get_html()
        # watch_dic = watch_price.parse_html()
        model, price, link = watch_price.parse_html(html_source)

        if price <= PRICE_LIMIT:
            body = f'Price on "{model}" is below ${PRICE_LIMIT}.\n\nVisit {BASIC_URL + link}'
            watch_price.send_email(body, smtp_address, port)
            break
        else:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(
                f'{current_date} - Price of cheapest "{model}" model is ${price} and still high.\n'
            )
        time.sleep(int(delay))


if __name__ == "__main__":
    main()
