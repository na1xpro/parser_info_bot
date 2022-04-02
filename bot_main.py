from lxml import html
import requests
from loguru import logger

url = (
    "https://www.olx.ua/elektronika/telefony-i-aksesuary/q-iphone-13/?search%5Bfilter_float_price%3Afrom%5D=10000&search%5Border%5D=created_at%3Adesc")


class Parser:
    def __init__(self, url, xpath):
        self.link_xpath = xpath
        self.url = url

    def find_links(self):
        response = requests.get(url)
        parsed_body = html.fromstring(response.text)
        link = parsed_body.xpath(self.link_xpath)
        return link

    def save_to_file_links(self):
        with open('text.txt', 'w') as file:
            for index in self.find_links():
                file.write(index + '\n')

    def checking_product_availability(self):
        links = self.find_links()
        with open('text.txt', 'r+') as opened_file:
            a = opened_file.read()
            for line in links:
                if line in a:
                    logger.info("Не найденно новых товаров")
                else:
                    opened_file.write(line)
                    logger.warning("Найден новый товар, был заменен в спсике.")


bot = Parser(
    "https://www.olx.ua/elektronika/telefony-i-aksesuary/q-iphone-13/?search%5Bfilter_float_price%3Afrom%5D=10000&search%5Border%5D=created_at%3Adesc",
    '//td[@class = "offer  "]/div[@class = "offer-wrapper"]/table/tbody/tr/td[2]/div/h3/a/@href')

logger.info("Parsing of all links from the site.")
bot.find_links()
logger.info("Adding links to a file.")
bot.save_to_file_links()
logger.info('Chek file in links')
bot.checking_product_availability()
