from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
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
            return jsonify(formatted_data)
        else:
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gbif_occurrences')
def gbif_occurrences():
    # Get country code from request arguments, default to Togo (TG)
    country_code = request.args.get('country', 'TG')

    # GBIF API URL for occurrences
    url = f"https://api.gbif.org/v1/occurrence/search?country={country_code}&limit=5"

    try:
        response = requests.get(url)
        data = response.json()

        if data and data['results']:
            # Clean and format the data
            formatted_data = []
            for entry in data['results']:
                formatted_data.append({
                    'species': entry.get('scientificName', 'N/A'),
                    'url': f"https://www.gbif.org/occurrence/{entry['key']}"
                })
            return jsonify(formatted_data)
        else:
            return jsonify({"error": "No data found for the selected criteria."}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
