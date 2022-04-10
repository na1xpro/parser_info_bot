from lxml import html
from loguru import logger
import requests
from datetime import datetime
import time
from bot_constants import constants


class Parser:
    def __init__(self, url, xpath_link, xpath_price):
        self.url = url
        self.link_xpath = xpath_link
        self.price_xpath = xpath_price

    def find_links_and_price(self):
        response = requests.get(self.url)
        parsed_body = html.fromstring(response.text)
        link = parsed_body.xpath(self.link_xpath)
        price = parsed_body.xpath(self.price_xpath)
        return link, price

    def save_to_file_links(self):
        links, prices = self.find_links_and_price()
        with open('text.txt', 'w') as file:
            for lin, pri in zip(links, prices):
                file.write(f"ID  Товару - | {lin} | Ціна товару - {pri} \n")
        return file

    def checking_product_availability(self):
        with open('text.txt', 'r+') as opened_file:
            a = opened_file.read()
            links, prices = self.find_links_and_price()
            for lines, pricess in zip(links, prices):
                if lines and pricess in a:
                    logger.info("Не знайдено нових товарів.")
                else:
                    self.save_to_file_links()
                    logger.warning("Знайдені нові товари, були замінені у файлі.")


bot = Parser(constants['URL'], constants['xpath_link'], constants['xpath_price'])

while True:
    now = datetime.now()
    logger.info("Парсинг посилань та цін із сайту.")
    bot.find_links_and_price()
    logger.info("Додавання посилань та цін у файл.")
    bot.save_to_file_links()
    logger.info("Посилання та ціни були додані до файлу.")
    logger.info('Перевірка на наявність нового товару.')
    bot.checking_product_availability()
    logger.warning("Останнє оновлення даних було" + str(now))
    time.sleep(60)
