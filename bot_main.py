from lxml import html
from loguru import logger
import requests
from datetime import datetime
import time
from bot_constants import constants
import sqlite3


class Parser:
    def __init__(self, url, xpath_link, xpath_price, ):
        self.url = url
        self.link_xpath = xpath_link
        self.price_xpath = xpath_price

    def find_links_and_price(self):
        response = requests.get(self.url)
        parsed_body = html.fromstring(response.text)
        index = parsed_body.xpath(self.link_xpath)
        price = parsed_body.xpath(self.price_xpath)
        return index, price

    def initialization_and_filling_the_base(self, data):
        index, price = data
        db = sqlite3.connect('base.db')
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS product(
            inde TEXT,
            price TEXT
        )""")
        db.commit()
        for ind, prices in zip(index, price):
            sql.execute("INSERT INTO product VALUES (?,?)", (ind, prices))
        db.commit()

bot = Parser(constants['URL'], constants['xpath_link'], constants['xpath_price'])
now = datetime.now()
logger.info("Парсинг посилань та цін із сайту.")
bot.find_links_and_price()
bot.initialization_and_filling_the_base(bot.find_links_and_price())
