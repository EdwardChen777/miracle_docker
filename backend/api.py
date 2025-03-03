from fastapi import FastAPI
import psycopg2
import pandas as pd
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# Allow requests from the frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change "*" to ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database connection using environment variables
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'miracle_scrap'),
    'user': os.getenv('DB_USER', 'edwardch'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'host': os.getenv('DB_HOST', 'db'),  # Use "db", not "localhost"
    'port': os.getenv('DB_PORT', '5432')
}

# queries the database 
def query_db(query):
    """Helper function to fetch data from PostgreSQL"""
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient='records')

# GET request: returns clinical trials grouped by sources 
@app.get("/api/total-trials")
def get_total_trials():
    """Returns total clinical trials from both sources"""
    query = "SELECT source, COUNT(*) AS total FROM transformed.combined_trials GROUP BY source;"
    return query_db(query)

# GET request: returns all clinical trials by condition
@app.get("/api/trials-by-condition")
def get_trials_by_condition():
    """Breakdown of clinical trials by condition"""
    query = "SELECT conditions, COUNT(*) AS count FROM transformed.combined_trials GROUP BY conditions ORDER BY count DESC;"
    return query_db(query)

# GET request: returns all clinical trials by sponsor
@app.get("/api/trials-by-sponsor")
def get_trials_by_sponsor():
    """Returns breakdown of trials by sponsor"""
    query = "SELECT sponsor, COUNT(*) AS count FROM transformed.combined_trials GROUP BY sponsor ORDER BY count DESC;"
    return query_db(query)