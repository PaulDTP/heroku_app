'''
@author Isaiah Terrell-Perica
@date 2/20/24

This file reads and writes data to a PostgreSQL database
'''
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os


if __name__ == "__main__":
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="zeppelin",
            user="isaiahtp",
            password=""
        )
        uri = "postgresql+psycopg2://isaiahtp@localhost:5432/zeppelin"
        engine = create_engine(uri)

        test = pd.read_parquet("../notebooks/ticks_test.parquet")
        test = test.iloc[:,:-3]
        test = test.applymap(lambda x: str(x) if isinstance(x, pd.Timedelta) else x)
        test.to_sql('smallticks', engine, index=False, if_exists='replace')


        query = "SELECT * FROM smallticks;"
        engine.execute(query)
        cursor = connection.cursor()
    finally:
        engine.dispose()

