CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.eu (
    id SERIAL PRIMARY KEY,
    study_identifier TEXT,
    study_title TEXT,
    conditions TEXT,
    sponsor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.us (
    id SERIAL PRIMARY KEY,
    study_identifier TEXT,
    study_title TEXT,
    conditions TEXT,
    sponsor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SCHEMA IF NOT EXISTS transformed;

CREATE TABLE IF NOT EXISTS transformed.combined_trials (
    id SERIAL PRIMARY KEY,
    study_identifier TEXT,
    study_title TEXT,
    conditions TEXT,
    sponsor TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);