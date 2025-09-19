from flask import Flask, jsonify
import requests
import os
from google.cloud import logging as cloud_logging

# Instantiates a client
logging_client = cloud_logging.Client()

# The name of the log to write to
log_name = "world-bank-api-logs"
# Selects the log to write to
logger = logging_client.logger(log_name)

app = Flask(__name__)

@app.route('/')
def home():
    logger.log_struct(
        {
            "message": "Home endpoint was accessed.",
            "component": "backend",
            "endpoint": "/",
        }
    )
    return "Welcome to the Environment Protection Software Backend!"

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
