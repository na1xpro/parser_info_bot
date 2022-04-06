import time

from lxml import html
from loguru import logger
import requests

from datetime import datetime


class Parser:
    def __init__(self, url, xpath_link, xpath_price):
        self.link_xpath = xpath_link
        self.url = url
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
                file.write(' ID  Товару - |' + lin + "| Цына товару " + pri + "\n")
        return file

    def checking_product_availability(self):
        with open('text.txt', 'r+') as opened_file:
            a = opened_file.read()
            links, prices = self.find_links_and_price()
            for lines, pricess in zip(links, prices):
                if lines and pricess in a:
                    logger.info("Не найденно новых товаров")
                else:
                    self.save_to_file_links()
                    logger.warning("Найденые новые твоары, были заменены в файле.")


bot = Parser(
    "https://www.olx.ua/uk/list/q-iphone/", '//table[@id = "offers_table"]//td[@class = "offer  "]//table/@data-id',
    '//table[@id = "offers_table"]//td[@class = "offer  "]//p[@class = "price"]/strong/text()')

while True:
    now = datetime.now()
    logger.info("Парсинг сылок и цен з сайта.")
    bot.find_links_and_price()
    logger.info("Добавление сылок и цен в файл.")
    bot.save_to_file_links()
    logger.info("Сылки и цены были добвленые.")
    logger.info('Проверка на наличие новых товаров')
    bot.checking_product_availability()
    logger.warning("Последнее обновление данных было " + str(now))
    time.sleep(60)
