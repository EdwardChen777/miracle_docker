from fastapi import FastAPI
import psycopg2
import pandas as pd

app = FastAPI()

# Database connection
DB_CONFIG = {
    'dbname': 'miracle_scrap',
    'user': 'edwardch',
    'password': '123456',
    'host': 'localhost',
    'port': '5434'
}

# queries the database 
def query_db(query):
    """Helper function to fetch data from PostgreSQL"""
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient='records')

# GET request: returns clinical trials grouped by sources 
@app.get("/total-trials")
def get_total_trials():
    """Returns total clinical trials from both sources"""
    query = "SELECT source, COUNT(*) AS total FROM transformed.combined_trials GROUP BY source;"
    return query_db(query)

# GET request: returns all clinical trials by condition
@app.get("/trials-by-condition")
def get_trials_by_condition():
    """Breakdown of clinical trials by condition"""
    query = "SELECT conditions, COUNT(*) AS count FROM transformed.combined_trials GROUP BY conditions ORDER BY count DESC;"
    return query_db(query)

# GET request: returns all clinical trials by sponsor
@app.get("/trials-by-sponsor")
def get_trials_by_sponsor():
    """Returns breakdown of trials by sponsor"""
    query = "SELECT sponsor, COUNT(*) AS count FROM transformed.combined_trials GROUP BY sponsor ORDER BY count DESC;"
    return query_db(query)