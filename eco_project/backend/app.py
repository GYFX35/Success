from flask import Flask, jsonify, request, send_from_directory
import requests
import os

# Mock logger for local development
class MockLogger:
    def log_struct(self, *args, **kwargs):
        pass  # Does nothing

# Conditionally initialize the logger
if os.environ.get('GAE_ENV') == 'standard':
    from google.cloud import logging as cloud_logging
    logging_client = cloud_logging.Client()
    log_name = "world-bank-api-logs"
    logger = logging_client.logger(log_name)
else:
    # Use a mock logger in local/non-GAE environments
    logger = MockLogger()

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/forest_area')
def forest_area():
    # World Bank API URL for forest area (% of land area) for Brazil, Indonesia, and Congo
    # Indicator: AG.LND.FRST.ZS
    # Countries: BRA (Brazil), IDN (Indonesia), COD (Congo, Dem. Rep.)
    url = "https://api.worldbank.org/v2/country/BRA;IDN;COD/indicator/AG.LND.FRST.ZS?format=json&date=2020"

    try:
        response = requests.get(url)
        data = response.json()

        # The API returns a list. The first element contains metadata, the second contains the data.
        if len(data) > 1 and data[1]:
            # Clean and format the data
            formatted_data = []
            for entry in data[1]:
                formatted_data.append({
                    'country': entry['country']['value'],
                    'country_iso3_code': entry['countryiso3code'],
                    'year': entry['date'],
                    'value': entry['value']
                })

            # Log the successful data fetch
            logger.log_struct(
                {
                    "message": "Successfully fetched forest area data.",
                    "component": "backend",
                    "endpoint": "/api/forest_area",
                },
                severity="INFO",
            )

            return jsonify(formatted_data)
        else:
            logger.log_struct(
                {
                    "message": "No data found for the selected criteria.",
                    "component": "backend",
                    "endpoint": "/api/forest_area",
                    "url": url,
                },
                severity="WARNING",
            )
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        logger.log_struct(
            {
                "message": f"Error fetching data from World Bank API: {e}",
                "component": "backend",
                "endpoint": "/api/forest_area",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/eu_forest_area')
def eu_forest_area():
    # Eurostat API URL for forest area for EU countries
    # Dataset: sdg_15_11
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_15_11?format=JSON&lang=en&time=2020"

    try:
        response = requests.get(url)
        data = response.json()

        if data and 'value' in data:
            # Clean and format the data
            formatted_data = []
            # Create a mapping from country code to country name
            geo_labels = data.get('dimension', {}).get('geo', {}).get('category', {}).get('label', {})

            # The API response has a flat list of values, and the order corresponds to the order of dimensions.
            # We need to iterate through the geo dimension to get the correct values.
            geo_categories = data.get('dimension', {}).get('geo', {}).get('category', {}).get('index', {})

            for country_code, index in geo_categories.items():
                value = data['value'][index]
                country_label = geo_labels.get(country_code, country_code) # Fallback to code if label not found
                formatted_data.append({
                    'country': country_label,
                    'country_code': country_code,
                    'year': '2020',
                    'value': value
                })

            # Log the successful data fetch
            logger.log_struct(
                {
                    "message": "Successfully fetched EU forest area data.",
                    "component": "backend",
                    "endpoint": "/api/eu_forest_area",
                },
                severity="INFO",
            )

            return jsonify(formatted_data)
        else:
            logger.log_struct(
                {
                    "message": "No data found for the selected criteria.",
                    "component": "backend",
                    "endpoint": "/api/eu_forest_area",
                    "url": url,
                },
                severity="WARNING",
            )
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        logger.log_struct(
            {
                "message": f"Error fetching data from Eurostat API: {e}",
                "component": "backend",
                "endpoint": "/api/eu_forest_area",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/agricultural_land')
def agricultural_land():
    # World Bank API URL for agricultural land (% of land area) for Brazil, Indonesia, and Congo
    # Indicator: AG.LND.AGRI.ZS
    # Countries: BRA (Brazil), IDN (Indonesia), COD (Congo, Dem. Rep.)
    url = "https://api.worldbank.org/v2/country/BRA;IDN;COD/indicator/AG.LND.AGRI.ZS?format=json&date=2020"

    try:
        response = requests.get(url)
        data = response.json()

        # The API returns a list. The first element contains metadata, the second contains the data.
        if len(data) > 1 and data[1]:
            # Clean and format the data
            formatted_data = []
            for entry in data[1]:
                formatted_data.append({
                    'country': entry['country']['value'],
                    'country_iso3_code': entry['countryiso3code'],
                    'year': entry['date'],
                    'value': entry['value']
                })

            # Log the successful data fetch
            logger.log_struct(
                {
                    "message": "Successfully fetched agricultural land data.",
                    "component": "backend",
                    "endpoint": "/api/agricultural_land",
                },
                severity="INFO",
            )

            return jsonify(formatted_data)
        else:
            # Log that no data was found
            logger.log_struct(
                {
                    "message": "No data found for the selected criteria.",
                    "component": "backend",
                    "endpoint": "/api/agricultural_land",
                    "url": url,
                },
                severity="WARNING",
            )
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        # Log the error
        logger.log_struct(
            {
                "message": f"Error fetching data from World Bank API: {e}",
                "component": "backend",
                "endpoint": "/api/agricultural_land",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    # Get Ollama API URL from environment variable or use default
    ollama_api_url = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")

    try:
        # Prepare the data for the Ollama API
        ollama_data = {
            "model": "gemma:2b",
            "prompt": user_message,
            "stream": False
        }

        # Send the request to the Ollama API
        response = requests.post(ollama_api_url, json=ollama_data)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the response from Ollama
        ai_response = response.json().get('response', "I'm sorry, I couldn't generate a response.")

        logger.log_struct(
            {
                "message": f"Chat message received: {user_message}",
                "response": ai_response,
                "component": "backend",
                "endpoint": "/api/chat",
            },
            severity="INFO",
        )

        return jsonify({"response": ai_response})

    except requests.exceptions.RequestException as e:
        logger.log_struct(
            {
                "message": f"Error communicating with Ollama API: {e}",
                "component": "backend",
                "endpoint": "/api/chat",
                "url": ollama_api_url,
            },
            severity="ERROR",
        )
        return jsonify({"error": "Failed to communicate with the AI service."}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)