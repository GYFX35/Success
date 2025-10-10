import json
import unittest
from unittest.mock import patch, Mock
from app import app
import requests

class ChildMortalityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')
    def test_child_mortality_success(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "structure": {
                "dimensions": {
                    "observation": [
                        {"id": "REF_AREA", "values": [{"id": "AFG", "name": "Afghanistan"}]},
                        {"id": "TIME_PERIOD", "values": [{"id": "2020", "name": "2020"}]}
                    ]
                }
            },
            "dataSets": [{
                "observations": {
                    "0:0": [100.0]
                }
            }]
        }
        mock_get.return_value = mock_response

        response = self.app.get('/api/child_mortality')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn('country', data[0])
        self.assertIn('country_code', data[0])
        self.assertIn('year', data[0])
        self.assertIn('value', data[0])
        self.assertEqual(data[0]['country'], 'Afghanistan')
        self.assertEqual(data[0]['country_code'], 'AFG')
        self.assertEqual(data[0]['year'], '2020')
        self.assertEqual(data[0]['value'], 100.0)

    @patch('app.requests.get')
    def test_child_mortality_no_data(self, mock_get):
        # Mock the API response for no data
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"dataSets": [{"observations": {}}]}
        mock_get.return_value = mock_response

        response = self.app.get('/api/child_mortality')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, [])

    @patch('app.requests.get')
    def test_child_mortality_api_error(self, mock_get):
        # Mock an API error
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        response = self.app.get('/api/child_mortality')
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {"error": "API is down"})

if __name__ == '__main__':
    unittest.main()