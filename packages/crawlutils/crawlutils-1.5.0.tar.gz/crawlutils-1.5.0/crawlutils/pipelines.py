import pymongo
from abc import ABC
from itemadapter import ItemAdapter


class MongoPipeline(ABC):
    def __init__(self, mongo_uri: str, mongo_db: str, collection_name: str):
        self.client = None
        self.db = None
        self.collection = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

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
