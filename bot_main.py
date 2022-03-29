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
        file = open('text.txt', 'w')
        for index in self.find_links():
            file.write(index + '\n')
        file.close()


bot = Parser(
    "https://www.olx.ua/elektronika/telefony-i-aksesuary/q-iphone-13/?search%5Bfilter_float_price%3Afrom%5D=10000&search%5Border%5D=created_at%3Adesc",
    "//a[@data-cy = 'listing-ad-title']/@href")

logger.info("Parsing of all links from the site.")
bot.find_links()
logger.info("Adding links to a file.")
bot.save_to_file_links()
