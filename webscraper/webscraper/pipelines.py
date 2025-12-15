# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import hashlib
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

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

    #every scraped item will be inserted in MongoDB and duplicates will be avoided
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_id = self.compute_item_id(adapter)
        
        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            raise DropItem(f"Duplicate item found: {adapter.get('url')}")
        else:
            item_dict = adapter.asdict()
            item_dict["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(item_dict)
            return item

    def compute_item_id(self, adapter):
        url = adapter.get("url")
        if not url:
            raise ValueError("Item must have 'url' field")
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

class WebscraperPipeline:
    def process_item(self, item, spider):
        return item
