# import logging
import psycopg
import pandas as pd
from pathlib import Path
import yaml


"""
Process database schema - steps: 
    1. Run in terminal: 
        docker run --name postgres_dmi -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=dmi_db -p 5433:5432 -d postgres

    2. lav config.yaml 
    
        db_config:
        name: dmi_db
        user: postgres
        password: 1234
        host: localhost
        port: 5433

    3. kør database script: python src/database/init_postgres_docker.py

"""


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.yaml"

with open(CONFIG_PATH, 'r') as file:
   config_yaml = yaml.safe_load(file)
   

db_config = config_yaml["db_config"]

conn_str = (
    f"dbname={db_config['name']} " 
    f"user={db_config['user']} "
    f"password={db_config['password']} "
    f"host={db_config['host']} "
    f"port={db_config['port']} "
    )


def create_db_schema(conn_str):
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute("""

                CREATE SCHEMA IF NOT EXISTS dmi;

                CREATE TABLE IF NOT EXISTS dmi.stations (
                    station_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100),
                    feature_id VARCHAR(100) UNIQUE
                );

                CREATE TABLE IF NOT EXISTS dmi.observations (
                    id SERIAL PRIMARY KEY,
                    feature_id VARCHAR(100) UNIQUE,
                    station_id VARCHAR(10) NOT NULL REFERENCES dmi.stations(station_id),
                    parameter_id VARCHAR(50) NOT NULL,
                    observed TIMESTAMPTZ NOT NULL,
                    value DOUBLE PRECISION NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

            """)

            conn.commit()

# Initialise database schema 
create_db_schema(conn_str)
