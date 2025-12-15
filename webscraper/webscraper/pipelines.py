# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

#wraps diff data containers
from itemadapter import ItemAdapter

class MongoPipeline:
    #MongoDB collection
    COLLECTION_NAME="Scrapeman"

    #initialize pipeline
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    #access to all core Scrapy components, such as the settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            #from items.py
            mongo_url=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    #every scraped item will be inserted in MongoDB
    def process_item(self, item, spider):
        self.db[self.COLLECTION_NAME].insert_one(item)
        return item

class WebscraperPipeline:
    def process_item(self, item, spider):
        return item
