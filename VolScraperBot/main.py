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
# import os
# import pymongo
# from itemadapter import ItemAdapter
# from scrapy.crawler import CrawlerProcess
# from spiders.NouvelairSpider import NouvelairSpider
# from spiders.TunisairExpressSpider import TunisairExpressSpider
# from spiders.AirfranceSpider import AirfranceSpider
# from spiders.TunisairSpider import TunisairSpider
# import concurrent.futures
# import signal  # Import signal module

# os.environ['TWISTED_REACTOR'] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# class MongoDBPipeline:
#     def __init__(self):
#         self.conn = pymongo.MongoClient('localhost', 27017)
#         db = self.conn['VolScraperBot_Data']
#         self.collection = db['vols']

#     def process_item(self, item, spider):
#         self.collection.insert_one(ItemAdapter(item).asdict())
#         return item

# def crawl_spider(SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date):
#     process = CrawlerProcess(settings={'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1}})
#     process.crawl(SpiderClass, place_of_departure=place_of_departure, place_of_arrival=place_of_arrival, type=type, check_in_date=check_in_date, check_out_date=check_out_date)
#     process.start()

# def install_signal_handlers():
#     signal.signal(signal.SIGTERM, signal.SIG_IGN)  # Ignore SIGTERM signal
#     signal.signal(signal.SIGINT, signal.SIG_IGN)   # Ignore SIGINT signal

# def main():
#     install_signal_handlers()  # Install signal handlers in the main thread
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

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         spider_classes = [ AirfranceSpider , NouvelairSpider , TunisairExpressSpider , TunisairSpider ]
#         futures = []
#         for SpiderClass in spider_classes:
#             futures.append(executor.submit(crawl_spider, SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date))
        
#         for future in concurrent.futures.as_completed(futures):
#             try:
#                 future.result()
#             except Exception as e:
#                 print("An error occurred:", e)

# if __name__ == "__main__":
#     main()
#********************séquentillement******************
# import os
# import pymongo
# from itemadapter import ItemAdapter
# from scrapy.crawler import CrawlerProcess
# from spiders.NouvelairSpider import NouvelairSpider
# from spiders.TunisairExpressSpider import TunisairExpressSpider
# from spiders.AirfranceSpider import AirfranceSpider
# from spiders.TunisairSpider import TunisairSpider
# import signal  # Import signal module

# os.environ['TWISTED_REACTOR'] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# class MongoDBPipeline:
#     def __init__(self):
#         self.conn = pymongo.MongoClient('localhost', 27017)
#         db = self.conn['VolScraperBot_Data']
#         self.collection = db['vols']

#     def process_item(self, item, spider):
#         self.collection.insert_one(ItemAdapter(item).asdict())
#         return item

# def crawl_spider(process, SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date):
#     process.crawl(SpiderClass, place_of_departure=place_of_departure, place_of_arrival=place_of_arrival, type=type, check_in_date=check_in_date, check_out_date=check_out_date)

# def install_signal_handlers():
#     signal.signal(signal.SIGTERM, signal.SIG_IGN)  # Ignore SIGTERM signal
#     signal.signal(signal.SIGINT, signal.SIG_IGN)   # Ignore SIGINT signal

# def main():
#     install_signal_handlers()  # Install signal handlers in the main thread
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

#     process = CrawlerProcess(settings={'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1}})
#     spider_classes = [AirfranceSpider, NouvelairSpider, TunisairExpressSpider, TunisairSpider]
#     for SpiderClass in spider_classes:
#         crawl_spider(process, SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date)
#     process.start()

# if __name__ == "__main__":
#     main()

#*******************************sémaphore***************
# import os
# import pymongo
# from itemadapter import ItemAdapter
# from scrapy.crawler import CrawlerProcess
# from spiders.NouvelairSpider import NouvelairSpider
# from spiders.TunisairExpressSpider import TunisairExpressSpider
# from spiders.AirfranceSpider import AirfranceSpider
# from spiders.TunisairSpider import TunisairSpider
# import signal  # Import signal module
# import threading  # Import threading module

# os.environ['TWISTED_REACTOR'] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# class MongoDBPipeline:
#     def __init__(self):
#         self.conn = pymongo.MongoClient('localhost', 27017)
#         db = self.conn['VolScraperBot_Data']
#         self.collection = db['vols']

#     def process_item(self, item, spider):
#         self.collection.insert_one(ItemAdapter(item).asdict())
#         return item

# def crawl_spider(SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date, semaphore):
#     process = CrawlerProcess(settings={'ITEM_PIPELINES': {'__main__.MongoDBPipeline': 1}})
#     process.crawl(SpiderClass, place_of_departure=place_of_departure, place_of_arrival=place_of_arrival, type=type, check_in_date=check_in_date, check_out_date=check_out_date)
#     process.start()
#     process.join()  # Wait for the spider process to finish
#     semaphore.release()  # Release semaphore after spider finishes

# def install_signal_handlers():
#     signal.signal(signal.SIGTERM, signal.SIG_IGN)  # Ignore SIGTERM signal
#     signal.signal(signal.SIGINT, signal.SIG_IGN)   # Ignore SIGINT signal

# def main():
#     install_signal_handlers()  # Install signal handlers in the main thread
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

#     semaphore = threading.Semaphore(1)  # Initialize semaphore with a count of 1

#     spider_classes = [AirfranceSpider, NouvelairSpider, TunisairExpressSpider, TunisairSpider]
#     for SpiderClass in spider_classes:
#         semaphore.acquire()  # Acquire semaphore before launching each spider
#         threading.Thread(target=crawl_spider, args=(SpiderClass, place_of_departure, place_of_arrival, type, check_in_date, check_out_date, semaphore)).start()

# if __name__ == "__main__":
#     main()
#****************************************************************************************
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
# from scrapy import signals
# from scrapy.signalmanager import dispatcher
# from spiders.NouvelairSpider import NouvelairSpider
# from spiders.TunisairExpressSpider import TunisairExpressSpider
# from spiders.AirfranceSpider import AirfranceSpider
# from spiders.TunisairSpider import TunisairSpider
# import pymongo

# def main():
#     configure_logging()
#     settings = get_project_settings()
#     runner = CrawlerRunner(settings)

#     # Fonction pour récupérer les arguments de l'utilisateur
#     def get_user_input():
#         place_of_departure = input("Entrez le lieu de départ : ")
#         place_of_arrival = input("Entrez le lieu d'arrivée : ")
#         travel_type = input("Entrez le type (aller-retour ou aller-simple) : ")

#         if travel_type == 'aller-retour':
#             check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
#             check_out_date = input("Entrez la date de retour (jj/mmm/aaaa) : ")
#         else:
#             check_in_date = input("Entrez la date et l'heure de départ (jj/mmm/aaaa) : ")
#             check_out_date = None

#         return {
#             'place_of_departure': place_of_departure,
#             'place_of_arrival': place_of_arrival,
#             'type': travel_type,
#             'check_in_date': check_in_date,
#             'check_out_date': check_out_date
#         }

#     # Fonction pour enregistrer les données dans MongoDB
#     def save_to_mongodb(data, collection_name):
#         client = pymongo.MongoClient("mongodb://localhost:27017/")
#         db = client["votre_base_de_donnees"]
#         collection = db[collection_name]
#         collection.delete_many({})  # Supprimer les données existantes
#         collection.insert_many(data)

#     @defer.inlineCallbacks
#     def crawl():
#         user_args = get_user_input()  # Obtenir les arguments de l'utilisateur
#         yield runner.crawl(NouvelairSpider, **user_args)
#         yield runner.crawl(TunisairExpressSpider, **user_args)
#         yield runner.crawl(TunisairSpider, **user_args)
#         yield runner.crawl(AirfranceSpider, **user_args)
#         reactor.stop()

#     # Connectez la fonction save_to_mongodb à chaque spider_closed signal
#     def spider_closed(spider, reason):
#         save_to_mongodb(spider.items, f"{spider.name}_collection")

#     dispatcher.connect(spider_closed, signal=signals.spider_closed)

#     crawl()
#     reactor.run()

# if __name__ == '__main__':
#     main()
#********************--------------------------------------------
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.NouvelairSpider import NouvelairSpider
from spiders.TunisairExpressSpider import TunisairExpressSpider
from spiders.AirfranceSpider import AirfranceSpider
from spiders.TunisairSpider import TunisairSpider

def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    # Fonction pour récupérer les arguments de l'utilisateur
    def get_user_input():
        place_of_departure = input("Entrez le lieu de départ : ")
        place_of_arrival = input("Entrez le lieu d'arrivée : ")
        travel_type = input("Entrez le type (aller-retour ou aller-simple) : ")

        if travel_type == 'aller-retour':
            check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
            check_out_date = input("Entrez la date de retour (jj/mmm/aaaa) : ")
        else:
            check_in_date = input("Entrez la date et l'heure de départ (jj/mmm/aaaa) : ")
            check_out_date = None

        return {
            'place_of_departure': place_of_departure,
            'place_of_arrival': place_of_arrival,
            'type': travel_type,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date
        }

    @defer.inlineCallbacks
    def crawl():
        user_args = get_user_input()  # Obtenir les arguments de l'utilisateur
        yield runner.crawl(NouvelairSpider, **user_args)
        yield runner.crawl(TunisairExpressSpider, **user_args)
        yield runner.crawl(TunisairSpider, **user_args)
        yield runner.crawl(AirfranceSpider, **user_args)
        reactor.stop()

    crawl()
    reactor.run()

if __name__ == '__main__':
    main()