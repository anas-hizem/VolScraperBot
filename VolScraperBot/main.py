import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Set event loop policy explicitly for Windows

from twisted.internet import asyncioreactor
asyncioreactor.install()

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

    def get_user_input():
        place_of_departure = input("Entrez le lieu de départ : ")
        place_of_arrival = input("Entrez le lieu d'arrivée : ")
        travel_type = input("Entrez le type (aller-retour ou aller-simple) : ")

        if travel_type == 'aller-retour':
            check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
            check_out_date = input("Entrez la date de retour (jj/mmm/aaaa) : ")
        else:
            check_in_date = input("Entrez la date de départ (jj/mmm/aaaa) : ")
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
        user_args = get_user_input() 
        yield runner.crawl(AirfranceSpider, **user_args)
        yield runner.crawl(NouvelairSpider, **user_args)
        yield runner.crawl(TunisairExpressSpider, **user_args)
        yield runner.crawl(TunisairSpider, **user_args)
        reactor.stop()

    crawl()
    reactor.run()

if __name__ == '__main__':
    main()
