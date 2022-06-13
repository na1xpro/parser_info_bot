from lxml import html
from loguru import logger
import requests
from bot_constants import constants
from lxml.html import fromstring
import sqlite3
import re


class Parser:
    def __init__(self, url):
        self.url = url
        self.name_database = 'base.db'
        self.conn, self.cursor = self.connect_database()

    def get_data(self):
        """Підклчюення парсера до сайту"""
        response = requests.get(self.url)
        tree = fromstring(response.text)
        return tree

    def parse_data(self, tree):
        """Парсинг данних з сайту"""
        product_list = []
        products = tree.xpath('//div[@data-cy="l-card"]')
        for product in products:
            top = product.xpath('.//div[@data-testid="adCard-featured"]')
            if not top:
                name = product.xpath(".//h6/text()")[0]
                price = product.xpath('.//div[@type="list"]/div/text()')
                for price_currency in price:
                    global currency
                    global new_price
                    currency = re.sub(r'\d+\s?', '', price_currency).strip()
                    new_price = re.sub(r'[а-я]+\s?', '', price_currency).strip()

                link = "https://www.olx.ua" + product.xpath(".//a/@href")[0]
                products_dict = {
                    "name": name,
                    "price": new_price,
                    'currency': currency,
                    "link": link,

                }
                product_list.append(products_dict)

        # print(product_list)
        return product_list

    def connect_database(self):
        """Підключення до бази данних"""
        conn = sqlite3.connect(self.name_database)
        cursor = conn.cursor()
        logger.info("Звязок з базою данних встановлено.")
        return conn, cursor

    def initialization_table(self):
        """Створення таблиці"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS product(
                    name TEXT,
                    price INT,
                    links TEXT,
                    currency TEXT
            )
            """)
        self.conn.commit()

    def filling_table(self, product_data: list[dict]):
        """Заповнення  данних в таблицю"""
        info = self.cursor.execute('SELECT * FROM product')
        if info.fetchone() is None:
            logger.info('Таблиця була не заповненою')
            for products in product_data:
                self.cursor.execute("INSERT INTO product VALUES (?,?,?,?)",
                                    (products['name'], products['price'], products['link'], products['currency']))
                self.conn.commit()
        else:
            logger.info('Таблиця вже заповнена')

    logger.info("Даннi були доданi до таблицi")

    def revision_new_data(self, products_data: list[dict]):
        """Перевірка  на актуальність данних"""
        for products in products_data:
            chek_link = self.cursor.execute(f"SELECT links FROM product WHERE links = '{products['link']}'")
            if chek_link.fetchone() is None:
                self.cursor.execute("""Update product set name = ?,price = ?,links = ?,currency = ?""", (
                    products['name'], products['price'], products['link'], products['currency']))
                self.conn.commit()
                logger.info('Був додадний новий товар')
            else:
                logger.info('Не було додано  нового товара')


#
#
bot = Parser(constants['URL'])
logger.info("Парсинг данних з сайту.")
product_data = bot.parse_data(bot.get_data())
bot.initialization_table()
bot.filling_table(product_data)
bot.revision_new_data(product_data)
