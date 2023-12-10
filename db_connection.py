import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def upsert_dataframe(df, table_name, engine):
    """
    Upserts a DataFrame into a PostgreSQL table.

    :param df: DataFrame to upsert.
    :param table_name: Name of the table where the DataFrame will be upserted.
    :param engine: SQLAlchemy engine object.
    """
    # Creating a temporary table
    temp_table_name = "temp_" + table_name
    df.head(0).to_sql(temp_table_name, engine, if_exists='replace', index=False)

    # Preparing the column names for the SQL query
    columns = df.columns.tolist()
    columns_str = ", ".join(columns)
    update_columns_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns])

    # SQL query for upsert
    sql = f"""
        INSERT INTO nebula_dev.{table_name} ({columns_str})
        SELECT * FROM {temp_table_name}
        ON CONFLICT title
        DO UPDATE SET
        {update_columns_str};
    """

    with engine.connect() as conn:
        conn.execute(sql)

    # Dropping the temporary table
    with engine.connect() as conn:
        conn.execute(f"DROP TABLE IF EXISTS {temp_table_name};")

