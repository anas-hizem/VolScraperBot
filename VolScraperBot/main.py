# import os
# import pymongo
# from itemadapter import ItemAdapter
# from scrapy.crawler import CrawlerProcess
# from spiders.NouvelairSpider import NouvelairSpider
# from spiders.TunisairExpressSpider import TunisairExpressSpider
# from spiders.AirfranceSpider import AirfranceSpider
# from spiders.TunisairSpider import TunisairSpider

# os.environ['TWISTED_REACTOR'] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# class MongoDBPipeline:
#     def __init__(self):
#         self.conn = pymongo.MongoClient('localhost', 27017)
#         db = self.conn['VolScraperBot_Data']
#         self.collection = db['vols']

#     def process_item(self, item, spider):
#         self.collection.insert_one(ItemAdapter(item).asdict())
#         return item

# def main():
#     conn = pymongo.MongoClient('localhost', 27017)
#     db = conn['VolScraperBot_Data']
#     collection = db['vols']
#     collection.delete_many({})
#     place_of_departure = input("Entrez le lieu de départ : ")
#     place_of_arrival = input("Entrez le lieu d'arrivée : ")
#     type = input("Entrez le type (aller-retour ou aller-simple) : ")
#     if type == 'aller-retour':
#         check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
#         check_out_date = input("Entrez la date de retour (jj/mmm/aaaa) : ")
#     else:
#         check_in_date = input("Entrez la date et l'heure de départ (jj/mmm/aaaa) : ")
#         check_out_date = None

#     process = CrawlerProcess(settings={
#         'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1},
#     })

#     for SpiderClass in [TunisairSpider , NouvelairSpider , AirfranceSpider , TunisairExpressSpider]:
#         process.crawl(SpiderClass, place_of_departure=place_of_departure, place_of_arrival=place_of_arrival, type=type, check_in_date=check_in_date, check_out_date=check_out_date)

#     process.start()

# if __name__ == "__main__":
#     main()


#****************************twisted******************************
# import os
# import pymongo
# from itemadapter import ItemAdapter
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from spiders.NouvelairSpider import NouvelairSpider
# from spiders.TunisairExpressSpider import TunisairExpressSpider
# from spiders.AirfranceSpider import AirfranceSpider
# from spiders.TunisairSpider import TunisairSpider
# from twisted.internet import reactor

# os.environ['TWISTED_REACTOR'] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# class MongoDBPipeline:
#     def __init__(self):
#         self.conn = pymongo.MongoClient('localhost', 27017)
#         db = self.conn['VolScraperBot_Data']
#         self.collection = db['vols']

#     def process_item(self, item, spider):
#         self.collection.insert_one(ItemAdapter(item).asdict())
#         return item

# def main():
#     conn = pymongo.MongoClient('localhost', 27017)
#     db = conn['VolScraperBot_Data']
#     collection = db['vols']
#     collection.delete_many({})
#     place_of_departure = input("Entrez le lieu de départ : ")
#     place_of_arrival = input("Entrez le lieu d'arrivée : ")
#     type = input("Entrez le type (aller-retour ou aller-simple) : ")
#     if type == 'aller-retour':
#         check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
#         check_out_date = input("Entrez la date de retour (jj/mmm/aaaa) : ")
#     else:
#         check_in_date = input("Entrez la date et l'heure de départ (jj/mmm/aaaa) : ")
#         check_out_date = None

#     configure_logging()
#     runner = CrawlerRunner()

#     for SpiderClass in [TunisairSpider, NouvelairSpider, AirfranceSpider, TunisairExpressSpider]:
#         runner.crawl(SpiderClass, place_of_departure=place_of_departure, place_of_arrival=place_of_arrival, type=type, check_in_date=check_in_date, check_out_date=check_out_date)

#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())

#     reactor.run()

# if __name__ == "__main__":
#     main()

#******************************concurrent.futures****************************
import os
import pymongo
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from spiders.NouvelairSpider import NouvelairSpider
from spiders.TunisairExpressSpider import TunisairExpressSpider
from spiders.AirfranceSpider import AirfranceSpider
from spiders.TunisairSpider import TunisairSpider
import concurrent.futures

os.environ['TWISTED_REACTOR'] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

class MongoDBPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        db = self.conn['VolScraperBot_Data']
        self.collection = db['vols']

    def process_item(self, item, spider):
        self.collection.insert_one(ItemAdapter(item).asdict())
        return item

def crawl_spider(SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date):
    process = CrawlerProcess(settings={'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1}})
    process.crawl(SpiderClass, place_of_departure=place_of_departure, place_of_arrival=place_of_arrival, type=type, check_in_date=check_in_date, check_out_date=check_out_date)
    process.start()

def main():
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['VolScraperBot_Data']
    collection = db['vols']
    collection.delete_many({})
    place_of_departure = input("Entrez le lieu de départ : ")
    place_of_arrival = input("Entrez le lieu d'arrivée : ")
    type = input("Entrez le type (aller-retour ou aller-simple) : ")
    if type == 'aller-retour':
        check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
        check_out_date = input("Entrez la date de retour (jj/mmm/aaaa) : ")
    else:
        check_in_date = input("Entrez la date et l'heure de départ (jj/mmm/aaaa) : ")
        check_out_date = None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        spider_classes = [AirfranceSpider ]
        futures = []
        for SpiderClass in spider_classes:
            futures.append(executor.submit(crawl_spider, SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("An error occurred:", e)

if __name__ == "__main__":
    main()
