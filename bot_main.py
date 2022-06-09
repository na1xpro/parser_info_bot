from lxml import html
from loguru import logger
import requests
from datetime import datetime
from bot_constants import constants
from lxml.html import fromstring
import sqlite3


class Parser:
    def __init__(self, url):
        self.url = url
        self.name_database = 'base.db'
        self.conn, self.cursor = self.connect_database()

    def unpack_dict(self, key_):
        unpack_list = []
        for iterator_key in product_data:
            key = iterator_key.get(key_)
            unpack_list.append(key)
        return unpack_list

    def parse_data(self):
        product_list = []
        response = requests.get(self.url)
        tree = fromstring(response.text)
        products = tree.xpath('//div[@data-cy="l-card"]')
        for product in products:
            top = product.xpath('.//div[@data-testid="adCard-featured"]')
            if not top:
                name = product.xpath(".//h6/text()")[0]
                price = product.xpath('.//div[@type="list"]/div/text()')
                price = price[0] if price else None
                link = "https://www.olx.ua" + product.xpath(".//a/@href")[0]
                for name_prod, price_prod, link_prod in zip([name], [price], [link]):
                    products_dict = {
                        "name": name_prod,
                        "price": price_prod,
                        "link": link_prod
                    }
                    product_list.append(products_dict)
        return product_list

    def connect_database(self):
        conn = sqlite3.connect(self.name_database)
        cursor = conn.cursor()
        logger.info("Звязок з базою данних встановлено.")
        return conn, cursor

    def initialization_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product(
                name TEXT,
                price TEXT,
                links TEXT
        )
        """)
        self.conn.commit()
        logger.info(" Таблиця додана ")

    def filling_table(self):
        for name, price, link in zip(self.unpack_dict('name'), self.unpack_dict('price'), self.unpack_dict('link')):
            self.cursor.execute("INSERT INTO product VALUES (?,?,?)", (name, price, link))
            self.conn.commit()

    logger.info("Даннi були доданi до таблицi")

    def revision_new_data(self):
        for name_prod in self.unpack_dict('name'):
            self.cursor.execute(f"SELECT name FROM product WHERE name = '{name_prod}'")
            if self.cursor.fetchone() is None:
                for name, price, link in zip(self.unpack_dict('name'), self.unpack_dict('price'),
                                             self.unpack_dict('link')):
                    self.cursor.execute("""Update product set name = ?,price = ?,links = ?""", (name, price, link))
                    self.conn.commit()
                    logger.info('Був додадний новий товар')
                else:
                    logger.info('Не було додано  нового товара')
                    self.conn.commit()


#
#
bot = Parser(constants['URL'])
now = datetime.now()
logger.info("Парсинг данних з сайту.")
product_data = bot.parse_data()
bot.initialization_table()
bot.filling_table()
bot.revision_new_data()
