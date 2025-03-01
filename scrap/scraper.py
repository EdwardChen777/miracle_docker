# importing modules
import requests
import pandas as pd
import os
from datetime import datetime
import time
from bs4 import BeautifulSoup
import csv
import psycopg2
import shutil
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def retrieve_latest_clinical_trials():
    # set up directories 
    curr_dir = os.getcwd()
    archive_dir = 'raw_data_archive'
    download_dir = os.path.join(curr_dir, 'download')
    download_path = os.path.join(download_dir, "ctg-studies.csv")
    
    # search for archive folders
    files = [f for f in os.listdir(archive_dir) if f.startswith("ctg-studies_") and f.endswith(".csv")]

    if not files:
        print("No archived files found.")
        return

    # Extract timestamps and sort by most recent
    files.sort(key=lambda f: time.strptime(re.search(r'_(\d{8}_\d{6})', f).group(1), "%Y%m%d_%H%M%S"), reverse=True)
    latest_file = files[0]
    latest_file_path = os.path.join(archive_dir, latest_file)
    
    # copy archive file to download path 
    shutil.copy(latest_file_path, download_path)
    print(f"Copied latest archive file: {latest_file_path} -> {download_path}")

def scrape_clinical_trials(download_dir, max_attempts=2):
    """Scrapes clinical trials data and retries on failure."""
    
    attempt = 0
    while attempt < max_attempts:
        try:
            print(f"Attempt {attempt + 1} of {max_attempts}...")

            # Setting up Selenium options
            options = Options()
            options.add_argument("--start-maximized") 
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--headless=new") 
            
            # Setting download preferences
            prefs = {
                "download.default_directory": download_dir,  
                "download.prompt_for_download": False,      
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True           
            }
            options.add_experimental_option("prefs", prefs)

            # Initializing WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://clinicaltrials.gov/search")

            try:
                # Accessing the download button
                main_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "action-bar-button"))
                )
                main_button.click()
                
                # Waiting for the download modal to pop up
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'usa-button') and contains(@class, 'primary-button')]"))
                )

                # Scroll down to access the download button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                time.sleep(1) 
                download_button.click()

                # Wait for the file to be downloaded
                timeout = 90 
                start_time = time.time()

                while time.time() - start_time < timeout:
                    files = os.listdir(download_dir)
                    crdownload_files = [f for f in files if f.endswith(".crdownload")]
                    if not crdownload_files:
                        completed_file = next((f for f in files if f.endswith(".csv")), None)
                        if completed_file:
                            print(f"File downloaded: {completed_file}")
                            driver.quit()
                            return completed_file
                    
                    time.sleep(1)

                print("Download did not complete within the expected time frame.")

            except (TimeoutException, NoSuchElementException) as e:
                print("Error while interacting with page elements:", e)
                raise  # Re-raise exception to trigger retry
            
            finally:
                driver.quit()
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(2 ** attempt)

    # download failed --> fetch archive
    print("All retry attempts failed. Going for archived files.")
    retrieve_latest_clinical_trials()
    return None
    
# scrapping a single page of eudraCT
def scrape_eudraCT_page(page, writer):
    URL = f"https://www.clinicaltrialsregister.eu/ctr-search/search?query=&page={page}"

    # retrieve website info
    response = requests.get(URL)

    # locate the tables wrapper containing the contents
    soup = BeautifulSoup(response.content, "html.parser")
    results_div = soup.find("div", class_="results")
    tables = results_div.find_all("table", class_="result")
            
    writer.writerow(["study_identifier", "sponsor", "study_title", "conditions"])

    # looping through each table and scrapping the information 
    for table_index, table in enumerate(tables, start=1):
        rows = table.find_all("tr")

        # Initialize variables to store extracted data
        study_identifier = sponsor_name = study_name = condition = "N/A"

        for row_index, row in enumerate(rows, start=1):
            # Get all table cells (td) within each row
            cells = row.find_all("td")
            row_data = [cell.text.strip() for cell in cells]  # Extract text from each cell
                    
            # Extract relevant data from each row
            if row_index == 1 and row_data:
                study_identifier = row_data[0].split(":")[1].strip()
            if row_index == 2 and row_data:
                sponsor_name = row_data[0].split(":")[1].strip() 
            if row_index == 3 and row_data:
                study_name = row_data[0].split(":")[1].strip() 
            if row_index == 4 and row_data:
                condition = row_data[0].split(":")[1].strip()

        # Write extracted data into the CSV file
        writer.writerow([study_identifier, sponsor_name, study_name, condition])
      
# scrapping multiple pages of eudraCT  
# end_page is inclusive
def scrape_eudraCT(file_name, start_page, end_page):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for page in range(start_page, end_page+1):
            scrape_eudraCT_page(page, writer)
    print(f"File downloaded: {file_name}")
          
# store csv into its respective table  
def store_csv(file_name, table_name):
    try:
        # Read CSV into a DataFrame
        df = pd.read_csv(file_name)
        
        # renaming EudraCT columns to match the format of clinicaltrials.gov
        if table_name == 'us':
            df.columns = ['study_identifier', 'study_title', 'study_url', 'status', 'conditions', 'interventions', 'sponsor', 'collaborators', 'study_type']

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname='miracle_scrap',
            user='edwardch',
            password='123456',
            host='localhost',
            port='5434'
        )
        cursor = conn.cursor()

        # Overwrite: Delete existing data before inserting new data
        cursor.execute(f"TRUNCATE TABLE raw.{table_name} RESTART IDENTITY;")
        conn.commit()
        print(f"Cleared existing data from {table_name}")

        # Insert new data
        for _, row in df.iterrows():
            cursor.execute(f"""
                INSERT INTO raw.{table_name} (study_identifier, study_title, conditions, sponsor)
                VALUES (%s, %s, %s, %s);
            """, (row['study_identifier'], row['study_title'], row['conditions'], row['sponsor']))

        conn.commit()
        print(f"Inserted {len(df)} records into {table_name}")

        # Close connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error when storing csv for {table_name}: {e}")
        
        
# move the downloaded raw data into archive folder
def archive_data():
    curr_dir = os.getcwd()
    download_dir = os.path.join(curr_dir, 'download')
    archive_dir = os.path.join(curr_dir, 'raw_data_archive')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Loop through all files in the download folder
    for filename in os.listdir(download_dir):
        old_path = os.path.join(download_dir, filename)

        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{timestamp}{ext}"  
        new_path = os.path.join(archive_dir, new_filename)
        shutil.move(old_path, new_path)
        
# combine data from us and eu into combined_trails table 
def combine_data():
    try:
        conn = psycopg2.connect(
            dbname='miracle_scrap',
            user='edwardch',
            password='123456',
            host='localhost',
            port='5434'  # Default PostgreSQL port
        )
        cursor = conn.cursor()

        # Step 1: Clear combined_trials table
        cursor.execute("TRUNCATE TABLE transformed.combined_trials RESTART IDENTITY;")

        # Step 2: Insert US trials
        cursor.execute("""
            INSERT INTO transformed.combined_trials (study_identifier, study_title, conditions, sponsor, source)
            SELECT study_identifier, study_title, conditions, sponsor, 'ClinicalTrials.gov' FROM raw.us;
        """)

        # Step 3: Insert EU trials
        cursor.execute("""
            INSERT INTO transformed.combined_trials (study_identifier, study_title, conditions, sponsor, source)
            SELECT study_identifier, study_title, conditions, sponsor, 'EudraCT' FROM raw.eu;
        """)

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print("Data successfully merged into transformed.combined_trials.")

    except Exception as e:
        print(f"Error during data transformation: {e}")
        
        
if __name__ == '__main__':
    
    # scrapping from ClinicalTrials.gov and first three pages of EudraCT
    curr_dir = os.getcwd()  
    download_dir = os.path.join(curr_dir,'download')
    us_file_name = os.path.join(download_dir, 'ctg-studies.csv')
    eu_file_name = os.path.join(download_dir, 'eudraCT.csv')
    start_page = 1
    end_page = 3
    
    scrape_clinical_trials(download_dir)
    scrape_eudraCT(eu_file_name, start_page, end_page)
    
    # storing the raw data into database 
    store_csv(us_file_name,'us')
    store_csv(eu_file_name,'eu')
    
    # move the downloaded csv into archive
    archive_data()
    
    # combining the raw data into combined_trial table
    combine_data()
    
    
    
    