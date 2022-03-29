from lxml import html
import requests

url = (
    "https://www.olx.ua/elektronika/telefony-i-aksesuary/q-iphone-13/?search%5Bfilter_float_price%3Afrom%5D=10000&search%5Border%5D=created_at%3Adesc")

class Parser:
    def __init__(self,xpath):
        self.xpath = xpath

    def find_link(self):
        response = requests.get(url)
        parsed_body = html.fromstring(response.text)
        link = parsed_body.xpath(self.xpath)
        return link


    def add_file_link(self):
        file = open('text.txt', 'w')
        for index in self.find_link():
            file.write(index + '\n')
        file.close()

bot = Parser("//a[@data-cy = 'listing-ad-title']/@href")
bot.find_link()
bot.add_file_link()
