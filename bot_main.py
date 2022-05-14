from lxml import html
from loguru import logger
import requests
from datetime import datetime
from bot_constants import constants
import sqlite3


class Parser:
    def __init__(self, url, id_product_xpath, xpath_price, links_product):
        self.url = url
        self.id_product_xpath = id_product_xpath
        self.price_xpath = xpath_price
        self.links_product = links_product
        self.name_database = 'base.db'
        self.conn, self.cursor = self.connect_database()

    def parse_data(self):
        response = requests.get(self.url)
        parsed_body = html.fromstring(response.text)
        ids_list = parsed_body.xpath(self.id_product_xpath)
        prices_list = parsed_body.xpath(self.price_xpath)
        links_prod = parsed_body.xpath(self.links_product)
        list_product = []
        products_id_price = {
        }
        products_links = {
        }
        links_key = "links"
        for id_prod, price_prod in zip(ids_list, prices_list):
            products_id_price[id_prod] = price_prod
        list_product.append(products_id_price)
        for prod_links in links_prod:
            products_links[prod_links] = links_key
        list_product.append(products_links)
        return list_product

    def connect_database(self):
        conn = sqlite3.connect(self.name_database)
        cursor = conn.cursor()
        logger.info("Звязок з базою данних встановлено.")
        return conn, cursor

    def initialization_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product(
                id_product INT,
                price TEXT,
                links TEXT
        )
        """)
        self.conn.commit()
        logger.info(" Таблиця додана ")

    def filling_table(self, product_data):
        for (index, prices), links in zip(product_data[0].items(), product_data[1].keys()):
            self.cursor.execute("INSERT INTO product VALUES (?,?,?)", (index, prices, links))
            self.conn.commit()
        logger.info("Даннi були доданi до таблицi")

    # def revision_new_data(self, product):
    #     for index, prices in product.items():
    #         self.cursor.execute("Update product set  id_product = ?, price = ?, status = 'NEWSW'", (index, prices))
    #         self.conn.commit()
    #     logger.info("Записи оновлені")



#
#
bot = Parser(constants['URL'], constants['xpath_id'], constants['xpath_price'], constants['xpath_links_product'])
now = datetime.now()
logger.info("Парсинг данних з сайту.")
product_data = bot.parse_data()
bot.initialization_table()
bot.filling_table(product_data)
