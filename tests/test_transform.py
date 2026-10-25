import unittest
from src.transform.transform import transform_stations, transform_observations, transform

'''
From root folder run in terminal: 
    python -m unittest discover -v

'''
# TO-DO OR DELETE
# class TestTransform(unittest.TestCase):

    
    # def test_transform(self):
    #     raw_data_stations = {
    #         "stations": 
    #         [
    #             {
    #             "id": "06070", 
    #             "name": "Station 1"
    #             }
    #         ]
    #     }
    #     raw_data_observations = {
    #         "observations": [
    #             {
    #                 "stationId": "06070",
    #                 "temperature": 20.5
    #             }
    #         ]
    #     }
    #     result = transform(raw_data_stations, raw_data_observations)
    #     self.assertIsInstance(result, dict)