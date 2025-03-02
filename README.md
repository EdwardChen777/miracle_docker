# Miracle Assessment

This project contains a **FastAPI backend**, a **React frontend** with **TailwindCSS** and **ReCharts**, and a **Python scraping script** that can be automated. The backend serves three API endpoints, while the frontend interacts with the backend and provides a simple dashboard to demonstrate the clinical trials data.

---

## Install App

```
git clone https://github.com/EdwardChen777/miracle.git
cd backend 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
deactivate
```
Open another terminal to serve the front end
```
cd frontend
npm install
npm run dev
```

## Running Web Scraping Script Locally
```
cd data
cd scrap
mkdir download && mkdir raw_data_archive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade webdriver-manager
python scraper.py
deactivate
```

## Building Docker Container for Web Scraping Script with PostgreSQL Database
```
cd data
docker-compose build
docker-compose up -d
```

## Setting Up Cron Job in Docker
Replace the last line of data/scrap/dockerfile
```
CMD ["python", "scraper.py"]
```
with the following
```
WORKDIR /app
RUN echo "*/45 * * * * python /app/scraper.py" > /etc/crontabs/root  # Runs scraper.py every 45 minutes
CMD ["crond", "-f"]
```

