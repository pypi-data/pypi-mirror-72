import pymongo
from itemadapter import ItemAdapter


class MongoPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.client = None
        self.db = None
        self.collection = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = self.__sanitize_item(item)

        self.collection.update_one({'_id': item['_id']},
                                   update={"$set": item},
                                   upsert=True)

        return item

    @staticmethod
    def __sanitize_item(item):
        dict_item = ItemAdapter(item).asdict()
        dict_item['_id'] = dict_item['id']
        dict_item.pop('id', None)

        return dict_item
