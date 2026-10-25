import unittest
from src.extract.extract import get_observations, get_query, get_stations


'''
From root folder run in terminal: 
    python -m unittest discover -v

'''

class TestExtract(unittest.TestCase):

    def test_get_query(self):
        
        api_service = "/v2/metObs/collections/station/items"
        params = {"stationId": "06070"}
        result = get_query(api_service, params)
        self.assertIsInstance(result, list[dict[str, any]])

    def test_get_query_no_params(self):
        api_service = "/v2/metObs/collections/station/items"
        result = get_query(api_service)
        self.assertIsInstance(result, list[dict[str, any]])

    def test_get_query_invalid_service(self):
        api_service = "/v2/metObs/collections/invalid/items"
        result = get_query(api_service)
        self.assertIsNone(result)

    def test_get_stations(self):
        result = get_stations()
        self.assertIsInstance(result, list[dict[str, any]])

    def test_get_query_metobs_invalid_date_params(self):
            result = get_query(
                api_service = "/v2/metObs/collections/observation/items", 
                params={
                    "stationId": "06070"
                    # , "limit": 10
                    , "datetime": "2020-01-01T00:00:00Z/2024-01-01T00:00:00Z"
                    , "period": "latest-month"
                    # , "offset": 400000
                    # , Add params
                    }
                )
            self.assertIsInstance(result, dict)