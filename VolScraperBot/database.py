from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['VolScraperBot_Data']
collection_demandes = db['demandes_de_recherche_de_vols']
collection_utilisateurs = db['utilisateurs']

def insert_user(data):
    if 'name' in data and 'email' in data and 'country' in data:
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'country': data['country']
        }
        insertion_result_user = collection_utilisateurs.insert_one(user_data)
        user_id = str(insertion_result_user.inserted_id)
        return user_id
    else:
        return None

def insert_flight_search_request(data, user_id):
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
    demande = str(insertion_result_demande.inserted_id)
    return demande
