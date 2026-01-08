from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
import requests
import os

# Mock logger for local development
class MockLogger:
    def log_struct(self, *args, **kwargs):
        pass  # Does nothing

# Conditionally initialize the logger
if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    from google.cloud import logging as cloud_logging
    logging_client = cloud_logging.Client()
    log_name = "world-bank-api-logs"
    logger = logging_client.logger(log_name)
else:
    # Use a mock logger in local/non-GAE environments
    logger = MockLogger()

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)

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
                # The Eurostat API response may not contain a value for every country,
                # so we need to check if the index exists in the 'value' object.
                value = data.get('value', {}).get(str(index))
                if value is not None:
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

@app.route('/api/drinking_water')
def drinking_water():
    # World Bank API URL for access to safely managed drinking water
    # Indicator: SH.H2O.SMDW.ZS
    # Countries: BRA (Brazil), IDN (Indonesia), COD (Congo, Dem. Rep.)
    url = "https://api.worldbank.org/v2/country/BRA;IDN;COD/indicator/SH.H2O.SMDW.ZS?format=json&date=2020"

    try:
        response = requests.get(url)
        data = response.json()

        if len(data) > 1 and data[1]:
            formatted_data = []
            for entry in data[1]:
                formatted_data.append({
                    'country': entry['country']['value'],
                    'country_iso3_code': entry['countryiso3code'],
                    'year': entry['date'],
                    'value': entry['value']
                })
            logger.log_struct(
                {
                    "message": "Successfully fetched drinking water data.",
                    "component": "backend",
                    "endpoint": "/api/drinking_water",
                },
                severity="INFO",
            )
            return jsonify(formatted_data)
        else:
            logger.log_struct(
                {
                    "message": "No data found for the selected criteria.",
                    "component": "backend",
                    "endpoint": "/api/drinking_water",
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
                "endpoint": "/api/drinking_water",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/energy_access')
def energy_access():
    # World Bank API URL for access to electricity
    # Indicator: EG.ELC.ACCS.ZS
    # Countries: BRA (Brazil), IDN (Indonesia), COD (Congo, Dem. Rep.)
    url = "https://api.worldbank.org/v2/country/BRA;IDN;COD/indicator/EG.ELC.ACCS.ZS?format=json&date=2020"

    try:
        response = requests.get(url)
        data = response.json()

        if len(data) > 1 and data[1]:
            formatted_data = []
            for entry in data[1]:
                formatted_data.append({
                    'country': entry['country']['value'],
                    'country_iso3_code': entry['countryiso3code'],
                    'year': entry['date'],
                    'value': entry['value']
                })
            logger.log_struct(
                {
                    "message": "Successfully fetched energy access data.",
                    "component": "backend",
                    "endpoint": "/api/energy_access",
                },
                severity="INFO",
            )
            return jsonify(formatted_data)
        else:
            logger.log_struct(
                {
                    "message": "No data found for the selected criteria.",
                    "component": "backend",
                    "endpoint": "/api/energy_access",
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
                "endpoint": "/api/energy_access",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500


@app.route('/api/life_expectancy')
def life_expectancy():
    # WHO OData API URL for Life expectancy at birth
    # Indicator: WHOSIS_000001
    url = "https://ghoapi.azureedge.net/api/WHOSIS_000001"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data and data.get('value'):
            formatted_data = []
            # Filter for specific countries and latest year available for each
            countries_of_interest = ["AFG", "ALB", "DZA"]
            latest_data = {}

            for record in data['value']:
                if record.get('SpatialDimType') == 'COUNTRY' and record.get('SpatialDim') in countries_of_interest and record.get('Dim1') == 'BTSX':
                    country = record['SpatialDim']
                    year = record['TimeDim']
                    value = record['NumericValue']

                    if country not in latest_data or year > latest_data[country]['year']:
                        latest_data[country] = {'year': year, 'value': value, 'country': country}

            formatted_data = list(latest_data.values())

            logger.log_struct(
                {
                    "message": "Successfully fetched life expectancy data.",
                    "component": "backend",
                    "endpoint": "/api/life_expectancy",
                },
                severity="INFO",
            )
            return jsonify(formatted_data)
        else:
            logger.log_struct(
                {
                    "message": "No data found for the selected criteria.",
                    "component": "backend",
                    "endpoint": "/api/life_expectancy",
                    "url": url,
                },
                severity="WARNING",
            )
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        logger.log_struct(
            {
                "message": f"Error fetching data from WHO API: {e}",
                "component": "backend",
                "endpoint": "/api/life_expectancy",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500


@app.route('/api/child_mortality')
def child_mortality():
    # UNICEF SDMX API URL for Child Mortality
    # Dataflow: UNICEF,CME,1.0
    # Countries: AFG (Afghanistan), ALB (Albania), DZA (Algeria)
    url = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,CME,1.0/AFG+ALB+DZA?format=sdmx-json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'dataSets' not in data or not data['dataSets'] or not data['dataSets'][0].get('observations'):
            return jsonify([])

        structure = data['structure']
        dimensions = structure['dimensions']['observation']

        # Find the index of each dimension
        dim_ids = [d['id'] for d in dimensions]
        try:
            country_dim_index = dim_ids.index('REF_AREA')
            time_dim_index = dim_ids.index('TIME_PERIOD')
        except ValueError:
            return jsonify({"error": "Could not find expected dimensions"}), 500

        # Get dimension values
        country_values = dimensions[country_dim_index]['values']
        time_values = dimensions[time_dim_index]['values']

        observations = data['dataSets'][0].get('observations', {})
        formatted_data = []

        for key, value_list in observations.items():
            indices = [int(i) for i in key.split(':')]

            country_code = country_values[indices[country_dim_index]]['id']
            country_name = country_values[indices[country_dim_index]]['name']
            year = time_values[indices[time_dim_index]]['id']
            value = value_list[0]

            formatted_data.append({
                'country': country_name,
                'country_code': country_code,
                'year': year,
                'value': value
            })

        logger.log_struct(
            {
                "message": "Successfully fetched and formatted child mortality data.",
                "component": "backend",
                "endpoint": "/api/child_mortality",
            },
            severity="INFO",
        )
        return jsonify(formatted_data)

    except requests.exceptions.RequestException as e:
        logger.log_struct(
            {
                "message": f"Error fetching data from UNICEF API: {e}",
                "component": "backend",
                "endpoint": "/api/child_mortality",
                "url": url,
            },
            severity="ERROR",
        )
        return jsonify({"error": str(e)}), 500

@app.route('/api/livestock')
def livestock():
    # This is a mocked endpoint due to the lack of a clear API for livestock data and an API key.
    mock_data = [
        {"country": "USA", "value": 94.4, "year": "2023"},
        {"country": "Brazil", "value": 215.2, "year": "2023"},
        {"country": "China", "value": 440.8, "year": "2023"},
        {"country": "EU", "value": 142.3, "year": "2023"}
    ]
    return jsonify(mock_data)

import json
import bleach
from filelock import FileLock

# Path for the videos JSON file and its lock file
VIDEOS_FILE = os.path.join(app.root_path, 'videos.json')
LOCK_FILE = os.path.join(app.root_path, 'videos.json.lock')

@app.route('/api/videos', methods=['GET', 'POST'])
def videos():
    if request.method == 'POST':
        # Handle video submission
        data = request.get_json()
        title = data.get('title')
        url = data.get('url')

        if not title or not url:
            return jsonify({"error": "Title and URL are required."}), 400

        # Sanitize user input
        sanitized_title = bleach.clean(title)
        sanitized_url = bleach.clean(url)

        # A simple check to ensure the URL is a YouTube embed URL
        if not sanitized_url.startswith("https://www.youtube.com/embed/"):
            return jsonify({"error": "Invalid YouTube URL."}), 400

        with FileLock(LOCK_FILE):
            # Read existing videos
            try:
                with open(VIDEOS_FILE, 'r') as f:
                    videos = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                videos = []

            # Add new video
            videos.append({"title": sanitized_title, "url": sanitized_url})

            # Write updated videos list back to the file
            with open(VIDEOS_FILE, 'w') as f:
                json.dump(videos, f, indent=4)

        return jsonify({"message": "Video added successfully!"}), 201

    else: # GET request
        # Return the list of videos
        with FileLock(LOCK_FILE):
            try:
                with open(VIDEOS_FILE, 'r') as f:
                    videos = json.load(f)
                return jsonify(videos)
            except (FileNotFoundError, json.JSONDecodeError):
                return jsonify([])

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

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('chat_message')
def handle_chat_message(message):
    emit('chat_message', message, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
