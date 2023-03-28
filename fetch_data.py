from os import getenv
from sqlalchemy import create_engine, text
import pandas as pd


def fetch(query):
    result = []
    try:
        # Create the SQLAlchemy engine
        engine = create_engine(getenv('RENDER_SQL_INT'), echo=True, future=True)
        # Define the query to select data from the table
        with engine.connect() as connection:
            result = connection.execute(text(query))
        result = pd.DataFrame(result.fetchall())
    except Exception as error:
        print(error)

    return result


if __name__ == '__main__':
    df = fetch('select * from ethzar_df')
    print(df)
