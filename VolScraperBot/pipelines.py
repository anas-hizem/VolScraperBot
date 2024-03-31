# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter

class MongoDBPipeline:
    def __init__(self):
        # Connectez-vous à MongoDB et sélectionnez la base de données et la collection
        self.conn = pymongo.MongoClient('localhost', 27017)
        db = self.conn['VolScraperBot_Data']
        self.collection = db['vols']

    def process_item(self, item, spider):
        # Convertissez l'item en un dictionnaire Python
        item_dict = ItemAdapter(item).asdict()
        # Insérez l'item dans la collection MongoDB
        self.collection.insert_one(item_dict)
        # Retournez l'item tel quel (sans modification)
        return item



