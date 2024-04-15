from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/search_flights', methods=['POST'])
def submit_form():
    data = request.json
    print(data)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    main_script_path = os.path.join(current_directory, 'C:/Users/HIZEM/Desktop/VolScraper/VolScraperBot/VolScraperBot/main.py')
    subprocess.Popen(['python', main_script_path , str(data)])
    return jsonify({"message": "Form submitted successfully"})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False, use_reloader=False)
