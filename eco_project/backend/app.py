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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
