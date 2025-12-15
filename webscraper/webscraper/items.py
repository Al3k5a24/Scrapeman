# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#object which we will scrape / change name by will
class FragranceItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    header = scrapy.Field()
    price_rsd = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    price_contact = scrapy.Field()
    pass
