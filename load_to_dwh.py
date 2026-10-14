import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/insurance_dwh"

engine = create_engine(DB_URL)

tables = [
    "policy_holders",
    "insurance_plans",
    "agents",
    "policies_sold",
    "claims"
]

def load_data():
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    for table in tables:
        df = pd.read_parquet(f"data_lake/raw_{table}.parquet")

        df.to_sql(
            table,
            engine,
            schema="raw",
            if_exists="replace",
            index=False
        )

        print(f"Завантажено {table}: {len(df)} записів")

    print("Усі таблиці успішно завантажені в PostgreSQL!")

if __name__ == "__main__":
    load_data()