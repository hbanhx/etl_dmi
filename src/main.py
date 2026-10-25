import logging
from pathlib import Path
from extract.extract import get_raw_data
from transform.transform import transform
from load.load import load_db

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "file.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"), 
        logging.StreamHandler()  # terminal output
    ]
)


if __name__ == "__main__":

    '''
    ETL setup and process:
    1. Setup config.yaml
        dir: /dmi/src/database/config.yaml

        example:
            db_config:
            name: dmi_db
            user: postgres
            password: 1234
            host: localhost
            port: 5433 

    3. Setup database:
        3.1 Run docker from terminal:
            docker run --name postgres_dmi -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=dmi_db -p 5433:5432 -d postgres
        
        3.2 Run def create_db_schema(conn_str)
            dir: /dmi/src/database/init_postgres_docker.py

    4. Run main.py

    '''
    logging.info("Starting ETL")
    
    logging.info("Starting extract process: Get raw data from API")
    raw_collections_station_items, raw_collections_observation_items = get_raw_data()

    logging.info("Starting transform process: Transform raw data")
    cleaned_dfs = transform(raw_collections_station_items, raw_collections_observation_items)

    logging.info("Starting load process: Load transformed data to database")
    load_db(cleaned_dfs)

    logging.info("ETL process finished")