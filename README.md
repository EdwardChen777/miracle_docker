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

## Web Scraping Script
```
cd scrap
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade webdriver-manager
python scraper.py
deactivate
```

## Setting Up Cron Job
Open up the terminal (make scraper run every 45 minutes)
```
crontab -e
```
Add the following to the file
```
*/45 * * * * /path/to/python3 /path/to/scrap/scraper.py
```

