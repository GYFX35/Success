from flask import Flask, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# Path for frontend static files
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('../frontend', path)

@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

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
            return jsonify(formatted_data)
        else:
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sdg_data')
def sdg_data():
    # UNDP API URL for SDG 15: Life on Land
    url = "https://api.open.undp.org/api/target-data.json?sdg=15"
    countries_of_interest = ["BRA", "IDN", "COD"]

    try:
        response = requests.get(url)
        data = response.json()

        if data:
            formatted_data = []
            for target in data:
                for recipient in target.get('top_recipients', []):
                    if recipient.get('iso3') in countries_of_interest:
                        formatted_data.append({
                            'country': recipient.get('name'),
                            'country_iso3_code': recipient.get('iso3'),
                            'target_id': target.get('target_id'),
                            'description': target.get('description'),
                            'budget': recipient.get('total_budget'),
                            'expense': recipient.get('total_expense')
                        })
            return jsonify(formatted_data)
        else:
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
