# Miracle Assessment

This project contains a **FastAPI backend**, a **React frontend** with **TailwindCSS** and **ReCharts**, and a **Python scraping script** that can be automated. The backend serves three API endpoints, while the frontend interacts with the backend and provides a simple dashboard to demonstrate the clinical trials data.

---

## Clone Repository
```
git clone https://github.com/EdwardChen777/miracle_docker.git
```

## Retrieving Data for archive folder 
Download data from **https://clinicaltrials.gov/search** and move to data/scrap/download
Add the current timestamp to it in the format of YYYYmmdd_hhmmss (e.g. ctg-studies_20250303_055829)

## Set up Docker Container
```
docker-compose up --build -d
```

## Close Docker Container
```
docker-compose down
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

## Outstanding Issue
The incompatibility between Chromedriver and Chrome is an outstanding issue, which requires manually downloading the CSV file and placing it in the archive folder.

