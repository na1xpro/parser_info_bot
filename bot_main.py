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

    def checking_product_availability(self):
        with open('text.txt', 'a+') as opened_file:
            for l in self.find_links():
                if l != opened_file:
                    logger.warning("YES new LINK")
                    opened_file.write(l)
                else:
                    logger.info('now new links')


# end_list = open('end_list.txt','w')
# listdir = open('listdir.txt')
# order_set = set(open('order_fix.txt').readlines())

# for line in listdir.readlines():
#    if line in order_set:
#        end_list.write(line)

bot = Parser(
    "https://www.olx.ua/elektronika/telefony-i-aksesuary/q-iphone-13/?search%5Bfilter_float_price%3Afrom%5D=10000&search%5Border%5D=created_at%3Adesc",
    "//a[@data-cy = 'listing-ad-title']/@href")

logger.info("Parsing of all links from the site.")
bot.find_links()
logger.info("Adding links to a file.")
bot.save_to_file_links()
logger.info('Chek file in links')
bot.checking_product_availability()
