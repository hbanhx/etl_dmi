import logging
import pandas as pd

"""
DMI: The validity period of each station occurance is denoted by the validFrom and validTo fields with validTo = null meaning no end time (forever).

"""

def transform_stations(collections_station_items: list[dict[str, any]]) -> pd.DataFrame:
    
    rows_stations = []
    for collection in collections_station_items:

        station_features = collection.get("features", [])
        logging.info(f"Station features: {len(station_features)}")  
        
        for feature in station_features:
            validTo = feature["properties"].get("validTo")
            if validTo is None:
                rows_stations.append({
                    "id": feature["id"], 
                    "stationId": feature["properties"].get("stationId"), 
                    "name": feature["properties"].get("name"), 
                    "validTo": feature["properties"].get("validTo")})
    df_stations = pd.DataFrame(rows_stations)
    logging.info(f"Station dataframe: rækker: {df_stations.shape[0]} | kolonner: {df_stations.shape[1]}")
    return df_stations


def transform_observations(collections_observation_items: list[dict[str, any]]) -> pd.DataFrame:
    
    rows_observations = []
    for collection in collections_observation_items:

        # features: list[] with feature: dict[str, any]
        observation_features = collection.get("features", [])
        logging.info(f"Observation features: {len(observation_features)}")
        
        for feature in observation_features:
            rows_observations.append({
                    "id": feature["id"],
                    "parameterId": feature["properties"].get("parameterId"), 
                    "stationId": feature["properties"].get("stationId"), 
                    "value": feature["properties"].get("value"), 
                    "observed": feature["properties"].get("observed")})
    df_observations = pd.DataFrame(rows_observations)
    logging.info(f"Observation dataframe: rækker: {df_observations.shape[0]} | kolonner: {df_observations.shape[1]}")
    return df_observations


# Transform raw data to clean DataFrames
def transform(raw_collections_station_items, raw_collections_observation_items) -> dict[str, pd.DataFrame]:

    logging.info("Transform raw stations data to dataframe")
    df_stations = transform_stations(raw_collections_station_items)

    logging.info("Transform raw observations data to dataframe")
    df_observations = transform_observations(raw_collections_observation_items)

    cleaned_dfs = {
       "stations": df_stations, 
       "observations": df_observations
       }

    logging.info("Finished transformation and returning dict[str, pd.DataFrame]")
    return cleaned_dfs