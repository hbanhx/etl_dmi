import logging
import sys # Exit app
import requests

# from tenacity import retry, stop_after_attempt, wait_random


'''
Meteorological Observation API

Swagger: 
    https://opendataapi.dmi.dk/v2/metObs/swagger-ui/index.html


Documentation API services
    https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api

API
/collections
Example: https://opendataapi.dmi.dk/v2/metObs/collections

Description: Will return all available collections in the API. Available collections:

- station
- observation

/collections/<collection name>/items
Query parameters

https://opendataapi.dmi.dk/v2/metObs/collections/station/items
https://opendataapi.dmi.dk/v2/metObs/collections/observation/items


'''

# Server API Service:
# base_url = "https://opendataapi.dmi.dk"

def get_query(api_service, params=None) -> list[dict[str, any]]:
    '''
    Set base URL for Server API:
        base_url = "https://opendataapi.dmi.dk"
    
    requests.get(url, params={key: value})
    '''
    
    base_url = "https://opendataapi.dmi.dk"
    url = f"{base_url}{api_service}"

    logging.info(f"Quering API Service: {base_url}{api_service}")
    logging.info(f"Parameters: {params}")
    collection_items = []
    try:

        while url:
            response = requests.get(f"{url}", params=params)
            response.raise_for_status() # If HTTP status code 200–299 (successful responses) continuem elseif 4xx (client error) or 5xx (server error), it raises an HTTPError
            r = response.json()
            logging.info(f"numberReturned: {r["numberReturned"]}")
            collection_items.append(r)

            url = None
            for link in r["links"]:
                if link.get("rel") == "next":
                    url = link.get("href")
                    params = None  # Reset params, already included in next url: "href"

                    break
        return collection_items
    
    except requests.exceptions.HTTPError as e:
        # Cast http errors
        logging.info(f"HTTP error: {e}")
        logging.info(f"Response text: {response.text}")
        sys.exit()  # If response (and data) not valid exit. 

    except requests.exceptions.RequestException as e:
        # Cast other errors
        logging.info(f"A request error occurred: {e}")
        sys.exit()


def get_stations() -> list[dict[str, any]]:
    '''
    Set query parameters and Get stations from API service

    station API Service:
        v2/metObs/collections/station/items
        
    Query String args: 
        params {key: value}:
        https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api   
    '''
    raw_collections_station_items = get_query(
        api_service = "/v2/metObs/collections/station/items", 
        params={
            # "stationId": "06070"
            # "limit": 1
            }
        )
    return raw_collections_station_items


def get_observations() -> list[dict[str, any]]:
    '''
    Set query parameters and Get observations from API service

    observation API Service:
        v2/metObs/collections/observation/items
        
    Query args: 
        params {key: value}:
        https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api   
    '''
    raw_collections_observation_items = get_query(
        api_service = "/v2/metObs/collections/observation/items", 
        params={
            "datetime": "2026-10-16T00:00:00Z/2026-10-16T23:59:59Z"
            # , "parameterId": "temp_dry"
            # "stationId": "06070"
            , "limit": 100000
            # , "period": "latest"
            # , "offset": 400000
            # , Add params
            }
        )
    return raw_collections_observation_items

# Extract raw data -> list[featureCollection]
def get_raw_data() -> tuple[list[dict[str, any]], list[dict[str, any]]]:
    
    logging.info("Get data: collections/station/items")
    raw_collections_station_items = get_stations()
    logging.info(type(raw_collections_station_items))

    logging.info("Get data: collections/observation/items")
    raw_collections_observation_items = get_observations()
    logging.info(type(raw_collections_observation_items))

    logging.info("Finished extract and returning raw data tuple[list[dict[str, any]], list[dict[str, any]]]")
    return raw_collections_station_items, raw_collections_observation_items