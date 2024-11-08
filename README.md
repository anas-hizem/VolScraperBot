
# VolScraperBot

VolScraperBot is a web application that allows users to search for flights based on their travel preferences. It utilizes Flask for the backend, Scrapy for web scraping, and MongoDB for data storage. The application collects user information and flight search requests, processes them, and retrieves flight data from various airline websites.

## Features

- User registration and flight search requests
- Scraping flight information from multiple airlines
- Storing user and flight search data in MongoDB
- API endpoints for submitting flight searches and checking scraping status
- Middleware for managing user-agent headers during scraping

## Technologies Used

- **Backend:** Flask
- **Web Scraping:** Scrapy
- **Database:** MongoDB
- **Python Libraries:** Flask-CORS, Twisted, Requests, Pymongo

## Installation

To run the application locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/VolScraperBot.git
    cd VolScraperBot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure you have MongoDB installed and running. The application connects to a MongoDB instance running on localhost.

5. Start the Flask application:
    ```bash
    python main.py
    ```

6. The API will be accessible at `http://localhost:5000`.

## API Endpoints

### Search Flights

- **POST** `/api/search_flights`
  - Submits a flight search request.
  - **Request Body:**
    ```json
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "country": "USA",
        "tripType": "aller-retour",
        "from": "New York",
        "to": "London",
        "startDateRoundTrip": "2024-12-01",
        "endDateValueRoundTrip": "2024-12-15",
        "startDateOneWay": null
    }
    ```
  - **Response:** 
    - Returns a success message upon submitting the flight search.

### Scraping Status

- **GET** `/api/scraping_status`
  - Checks the current status of the scraping process.
  - **Response:** 
    ```json
    {
        "status": "scraping_in_progress" | "scraping_finished"
    }
    ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes you'd like to propose.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the developers of Flask, Scrapy, and MongoDB for their excellent frameworks and tools.

