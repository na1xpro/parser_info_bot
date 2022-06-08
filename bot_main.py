from lxml import html
from loguru import logger
import requests
from datetime import datetime
from bot_constants import constants
import sqlite3


class Parser:
    def __init__(self, url, name_product_xpath, xpath_price, links_product, ):
        self.url = url
        self.id_product_xpath = name_product_xpath
        self.price_xpath = xpath_price
        self.links_product = links_product
        # self.addition_data = addition_data #Надо доабвить в инициализацию
        self.name_database = 'base.db'
        self.url_website = "https://www.olx.ua"
        self.conn, self.cursor = self.connect_database()

    def parse_data(self):
        response = requests.get(self.url)
        parsed_body = html.fromstring(response.text)
        name_prod_list = parsed_body.xpath(self.id_product_xpath)
        prices_list = parsed_body.xpath(self.price_xpath)
        links_prod = parsed_body.xpath(self.links_product)
        # addition_data = parsed_body.xpath(self.addition_data)
        products_data_list = []
        for id_prod, price_prod, link_prod in zip(name_prod_list, prices_list, links_prod, ):
            products_dict = {
                "name_prod": id_prod,
                "price": price_prod,
                "link": self.url_website + link_prod,
                # 'ad_info': add_data
            }
            products_data_list.append(products_dict)
        print(products_data_list)
        return products_data_list

    def connect_database(self):
        conn = sqlite3.connect(self.name_database)
        cursor = conn.cursor()
        logger.info("Звязок з базою данних встановлено.")
        return conn, cursor

    def initialization_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product(
                name_product INT,
                price TEXT,
                links TEXT
        )
        """)
        self.conn.commit()
        logger.info(" Таблиця додана ")

    def filling_table(self, product_data):
        def unpack_dict(key_):
            test = []
            for iterator_key in product_data:
                key = iterator_key.get(key_)
                test.append(key)
            return test

        for name, price, link in zip(unpack_dict('name_prod'), unpack_dict('price'), unpack_dict('link')):
            self.cursor.execute("INSERT INTO product VALUES (?,?,?)", (name, price, link))
            self.conn.commit()

    logger.info("Даннi були доданi до таблицi")


# def revision_new_data(self, product):
#     for index, prices in product.items():
#         self.cursor.execute("Update product set  id_product = ?, price = ?, status = 'NEWSW'", (index, prices))
#         self.conn.commit()
#     logger.info("Записи оновлені")


#
#
bot = Parser(constants['URL'], constants['xpath_name'], constants['xpath_price'], constants['xpath_links_product'])
now = datetime.now()
logger.info("Парсинг данних з сайту.")
product_data = bot.parse_data()
bot.initialization_table()
bot.filling_table(product_data)
