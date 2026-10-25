import logging
import psycopg
import yaml
from pathlib import Path


"""
Process database schema - steps: 
1: Run in terminal:
    docker run --name postgres_dmi -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=dmi_db -p 5433:5432 -d postgres

2. lav config.yaml 
 
    db_config:
    name: dmi_db
    user: postgres
    password: 1234
    host: localhost
    port: 5433

3. kør database script: 
    python scr/database/postgres_docker.py

    RETURNING feature_id;

"""

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "database"
CONFIG_PATH = DATA_DIR / "config.yaml"

with open(CONFIG_PATH, 'r') as file:
   config_yaml = yaml.safe_load(file)

db_config = config_yaml["db_config"]


def connnection_string():
    conn_str = (
        f"dbname={db_config['name']} " 
        f"user={db_config['user']} "
        f"password={db_config['password']} "
        f"host={db_config['host']} "
        f"port={db_config['port']} "
        )
    return conn_str

# Load clean DataFrames to database
def load_db(cleaned_dfs):
    conn_str =  connnection_string()
    with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:

                # Iterate DataFrame rows
                logging.info(f"stations data: {cleaned_dfs['stations'].shape[0]} rows")
                count_stations_inserted = 0
                count_stations_skipped = 0
                for _, row in cleaned_dfs["stations"].iterrows():
                    try:
                        cur.execute(
                            """
                            INSERT INTO dmi.stations (station_id, name, feature_id) 
                            VALUES (%s, %s, %s) 
                            ON CONFLICT (feature_id) DO NOTHING
                            RETURNING feature_id;
                            """,
                            (row["stationId"], row["name"], row["id"])
                        )
                        conn.commit()
                        result = cur.fetchone() # fetchone() returns row (first row in table), but returns "None" "ON CONFLICT"
                        if result:
                            count_stations_inserted += 1
                        else:
                            count_stations_skipped += 1
                    except Exception as e:
                        logging.info(f"Row skipped due to error: {e} - transaction rolled back and continue")
                        cur.rollback() # Roll back transaction error state and continue next row
                        continue


                count_observations_inserted = 0
                count_observations_skipped = 0
                for _, row in cleaned_dfs["observations"].iterrows():
                    try:
                        cur.execute(
                            """
                            INSERT INTO dmi.observations (station_id, feature_id, parameter_id, observed, value)
                            VALUES (%s, %s, %s, %s, %s) 
                            ON CONFLICT (feature_id) DO NOTHING
                            RETURNING feature_id;
                            """,
                            (row["stationId"], row["id"], row["parameterId"], row["observed"], row["value"])
                        )
                        conn.commit()
                        result = cur.fetchone()
                        if result:
                            count_observations_inserted += 1
                        else:
                            count_observations_skipped += 1
                    except Exception as e:
                        logging.info(f"Row skipped due to error: {e} - transaction rolled back and continue")
                        cur.rollback()
                        continue

                logging.info("Load finished")
                logging.info(f"Stations: inserted {count_stations_inserted} | skipped {count_stations_skipped}")
                logging.info(f"Observations: inserted {count_observations_inserted} | skipped {count_observations_skipped}")