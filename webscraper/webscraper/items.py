# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FragranceItem(scrapy.Item):

    link = scrapy.Field()
    header = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    pass
