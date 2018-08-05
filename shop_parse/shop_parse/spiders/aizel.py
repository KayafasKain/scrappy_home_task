import scrapy
import re
from ..items import ShopParseItem

class AizelSpider(scrapy.Spider):
    name = 'aizel'
    start_urls = ['https://aizel.ru/ua-ru/odezhda', 'https://aizel.ru/ua-ru/obuv/']


    def parse(self, response): # parsing manin page
        requests = 0
        for href in response.xpath('//li[contains(@class, "product__item")]//a/@href').extract():
            if requests < 1:
                link = 'https://aizel.ru' + href
                yield scrapy.Request(link, callback=self.parse_sizes, meta={'link': link})
            else:
                break
            requests += 1

    def parse_sizes(self, response):
        link = response.meta.get('link')
        id = re.search('[0-9]+', link)
        link = 'https://aizel.ru/products/sizes/?id=' + id.group(0)
        yield scrapy.Request(link, callback=self.parse_category, meta={'page_response': response})

    def parse_category(self, response):
        item = ShopParseItem()
        page_response = response.meta.get('page_response')
        item['ware_name'] = self.parse_ware_name(page_response)
        item['price'] = self.parse_price(page_response)
        item['currency'] = self.parse_currency(page_response)
        item['description'] = self.parse_description(page_response)
        item['images'] = self.parse_images(page_response)
        item['brand'] = self.parse_brand(page_response)
        item['sizes'] = self.parse_clth_size(response)
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

    def parse_clth_size(self, response):
        return response.selector.xpath(
            '//ul[contains(@class, "product-size__list scrolling")]//' +
            'span[contains(@class, "product-size-title")]/text()'
        ).extract()