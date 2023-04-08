from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, inspect


def fetch(query):
    result = []
    try:
        # Create the SQLAlchemy engine
        engine = create_engine('sqlite:///data.db', echo=True, future=True)

        # Define the query to select data from the table
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            if not inspect(engine).has_table('trade_table'):  # If table don't exist, Create.
                metadata = MetaData()
                # Create a table with the appropriate Columns
                Table(
                    'trade_table',
                    metadata,
                    Column('order_id', String(50), primary_key=True),
                    Column('price', Float)
                )
                # Implement the creation
                metadata.create_all(connection)
            result = connection.execute(query)
            print('Writing to DB')
        # result = pd.DataFrame(result.fetchall())
    except Exception as error:
        print(error)

    return result


if __name__ == '__main__':
    df = fetch('select * from ethzar_df')
    print(df)
