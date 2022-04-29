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
        self.name_save_file = 'text.txt'
        self.links = self.find_links_and_price()

    def find_links_and_price(self):
        response = requests.get(self.url)
        parsed_body = html.fromstring(response.text)
        index = parsed_body.xpath(self.link_xpath)
        price = parsed_body.xpath(self.price_xpath)
        return index, price

    def save_to_file_links(self):
        with open(self.name_save_file, 'w') as file:
            for lin, pri in zip(self.links):
                file.write(f"ID  Товару - | {lin} | Ціна товару - {pri} \n")

    def chek_in_file(self, data):
        links, prices = data
        with open(self.name_file, 'r+') as file:
            a = file.read()
            for lines, pricess in zip(links, prices):
                if lines and pricess in a:
                    logger.info("Не знайдено нових товарів.")
                else:
                    file.write(f"ID  Товару - | {lines} | Ціна товару - {pricess} - НОВИЙ ТОВАР \n")
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
    bot.chekinfile(bot.find_links_and_price())
    logger.warning("Останнє оновлення даних було" + str(now))
    time.sleep(60)
