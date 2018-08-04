import scrapy
from ..items import ShopParseItem

class AizelSpider(scrapy.Spider):
    name = 'aizel'
    start_urls = ['https://aizel.ru/ua-ru/odezhda', 'https://aizel.ru/ua-ru/obuv/']


    def parse(self, response): # parsing manin page
        requests = 0
        for href in response.xpath('//li[contains(@class, "product__item")]//a/@href').extract():
            if requests < 1:
                yield scrapy.Request('https://aizel.ru' + href, callback=self.parse_category)
            else:
                break
            requests += 1

    def parse_category(self, response):
        item = ShopParseItem()
        item['ware_name'] = self.parse_ware_name(response)
        item['price'] = self.parse_price(response)
        item['currency'] = self.parse_currency(response)
        item['description'] = self.parse_description(response)
        item['images'] = self.parse_images(response)
        item['brand'] = self.parse_brand(response)
        yield item

    def parse_ware_name(self, response):
        return response.selector.xpath(
            '//div[contains(@class, "product-item__header")]/h1[contains(@class, "product-item__name-desc")]/@content'
            ).extract()

    def parse_price(self, response):
        return response.selector.xpath(
            '//div[contains(@class, "product-item__header")]//div[contains(@class, "product__desc__price product__desc__price_int")]' +
            '/span/text()'
        ).extract()

    def parse_currency(self, response):
        return response.selector.xpath(
            '//div[contains(@class, "product-item__header")]//div[contains(@class, "product__desc__price product__desc__price_int")]' +
            '/span/@data-symbol'
        ).extract()

    def parse_description(self, response):
        return response.selector.xpath(
            '//div[contains(@class, "accordion__item__content")]/p/text()'
        ).extract()

    def parse_images(self, response):
        return response.selector.xpath(
            '//li[contains(@class, "carousel__item")]/a/@data-zoom'
        ).extract()

    def parse_brand(self, response):
        return response.selector.xpath(
            '//div[contains(@class, "product-item__header")]/a[contains(@class, "product-item__name")]/text()'
            ).extract()