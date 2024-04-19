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


from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['VolScraperBot_Data']
collection_demandes = db['demandes_de_recherche_de_vols']
collection_utilisateurs = db['utilisateurs']

@app.route('/api/search_flights', methods=['POST'])
def submit_form():
    data = request.json    
    print(data)
    if 'name' in data and 'email' in data and 'country' in data:
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'country': data['country']
        }
        insertion_result_user = collection_utilisateurs.insert_one(user_data)
        user_id = str(insertion_result_user.inserted_id)
        demande_data = {
            'user_id': user_id,
            'tripType': data['tripType'],
            'from': data['from'],
            'to': data['to'],
            'startDateRoundTrip': data.get('startDateRoundTrip', None),
            'endDateValueRoundTrip': data.get('endDateValueRoundTrip', None),
            'startDateOneWay': data.get('startDateOneWay', None)
        }
        insertion_result_demande = collection_demandes.insert_one(demande_data)
        demande_id = str(insertion_result_demande.inserted_id)
        main(data, demande_id) 
        return jsonify({"message": "Form submitted successfully"})
    else:
        demande_data = {
            'tripType': data['tripType'],
            'from': data['from'],
            'to': data['to'],
            'startDateRoundTrip': data.get('startDateRoundTrip', None),
            'endDateValueRoundTrip': data.get('endDateValueRoundTrip', None),
            'startDateOneWay': data.get('startDateOneWay', None)
        }
        insertion_result_demande = collection_demandes.insert_one(demande_data)
        demande_id = str(insertion_result_demande.inserted_id)
        main(data, demande_id) 
        return jsonify({"message": "Form submitted successfully"})



def main(data, demande_id):
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    def get_user_input(data):
        place_of_departure = data['from']
        place_of_arrival = data['to']
        travel_type = data['tripType']
        check_in_date = data['startDateRoundTrip'] if travel_type == 'aller-retour' else data['startDateOneWay']
        check_out_date = data['endDateValueRoundTrip'] if travel_type == 'aller-retour' else None

        return {
            'place_of_departure': place_of_departure,
            'place_of_arrival': place_of_arrival,
            'type': travel_type,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date
        }

    @defer.inlineCallbacks
    def crawl():
        user_args = get_user_input(data)
        user_args['demande_id'] = demande_id

        # Ajoutez un timeout pour chaque spider
        timeout_seconds = 60  # Par exemple, 60 secondes
        timeout_deferred = reactor.callLater(timeout_seconds, reactor.stop)


        yield runner.crawl(AirfranceSpider, **user_args)
        yield runner.crawl(NouvelairSpider, **user_args)
        yield runner.crawl(TunisairSpider, **user_args)
        yield runner.crawl(TunisairExpressSpider, **user_args)

    # Annulez le timeout après que tous les spiders ont été lancés
        if not timeout_deferred.called:
            timeout_deferred.cancel()

        reactor.stop()

    crawl()
    reactor.run()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False, use_reloader=True )
