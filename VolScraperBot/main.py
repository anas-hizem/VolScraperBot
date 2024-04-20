from flask import Flask, request, jsonify
from flask_cors import CORS
from database import insert_user, insert_flight_search_request
from scraping import run_scraping

app = Flask(__name__)
CORS(app)

# Variable globale pour stocker l'état du scraping
scraping_in_progress = False

@app.route('/api/search_flights', methods=['POST'])
def submit_form():
    global scraping_in_progress
    data = request.json    
    print(data)
    user_id = insert_user(data)
    demande_id = insert_flight_search_request(data, user_id)
    scraping_in_progress = True
    run_scraping(data, demande_id)
    scraping_in_progress = False
    return 'Flight search submitted successfully'

@app.route('/api/scraping_status', methods=['GET'])
def scraping_status():
    global scraping_in_progress
    return jsonify({'status': 'scraping_in_progress' if scraping_in_progress else 'scraping_finished'})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False, use_reloader=True)
