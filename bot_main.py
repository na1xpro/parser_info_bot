from lxml import html
from loguru import logger
import requests
from datetime import datetime
from bot_constants import constants
import sqlite3


class Parser:
    def __init__(self, url, xpath_link, xpath_price, ):
        self.url = url
        self.link_xpath = xpath_link
        self.price_xpath = xpath_price
        self.name_database = 'base.db'
        self.sql_cursor, self.db = self.connect_database()
        self.ind, self.pric = self.find_links_and_price()

    def find_links_and_price(self):
        response = requests.get(self.url)
        parsed_body = html.fromstring(response.text)
        index = parsed_body.xpath(self.link_xpath)
        price = parsed_body.xpath(self.price_xpath)
        return index, price

    def connect_database(self):
        db = sqlite3.connect(self.name_database)
        sql = db.cursor()
        logger.info("Звязок з базою данних встановлено.")
        return sql, db

    def initialization_and_filling_the_base(self):
        self.sql_cursor.execute("""CREATE TABLE IF NOT EXISTS product(
                indeх TEXT,
                price TEXT,
                status TEXT
    
            )""")
        self.db.commit()
        for ind, prices in zip(self.ind, self.pric):
            self.sql_cursor.execute("INSERT INTO product VALUES (?,?,?)", (ind, prices, "NEW"))
        self.db.commit()
        logger.info("Данн доданы")

    def revision_new_data(self):
        for ind, prices in zip(self.ind, self.pric):
            self.sql_cursor.execute("Update product set  indeх = ?,price = ?,status = 'NEWSW'", (ind, prices))
            self.db.commit()
        logger.info("Записи оновлений")


#
#
bot = Parser(constants['URL'], constants['xpath_link'], constants['xpath_price'])
now = datetime.now()
logger.info("Парсинг посилань та цін із сайту.")
bot.find_links_and_price()
# bot.initialization_and_filling_the_base()
bot.revision_new_data()
