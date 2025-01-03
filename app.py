from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import uuid
import random
import time

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["stir_tech_internship"]  # Database name
collection = db["trending_topics"]  # Collection name

# Load proxy list
PROXY_LIST = []
with open("valid_proxies_server.txt", "r") as f:
    PROXY_LIST = [proxy.strip() for proxy in f.readlines() if proxy.strip()]

def get_driver(proxy):
    """Initialize a Selenium WebDriver with a given proxy."""
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def save_to_mongo(record):
    """Save a record to MongoDB."""
    collection.insert_one(record)

def fetch_trending_topics():
    """Fetch trending topics using Selenium and save them to MongoDB."""
    proxy = random.choice(PROXY_LIST)
    driver = get_driver(proxy)
    trends = []
    ip_address = proxy

    try:
        driver.get("https://x.com/i/flow/login")  # Log in required
        time.sleep(4)  # Wait for the page to load

        # Login process
        email_em = driver.find_element(By.XPATH, "//input[@name='text']")
        email_em.send_keys("karmakarri80145")
        time.sleep(1)
        next_em = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        next_em.click()
        time.sleep(3)
        try:
            pass_em = driver.find_element(By.XPATH, "//input[@name='password']")
            pass_em.send_keys("..operation")
            time.sleep(1)
        except:
            time.sleep(120)
            pass_em = driver.find_element(By.XPATH, "//input[@name='password']")
            pass_em.send_keys("..operation")
            time.sleep(1)
        finally:
            login_em = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
            login_em.click()
            time.sleep(7)
        time.sleep(70)
        
        trending_elements = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")
        trends = [elem.text for elem in trending_elements[1::3]]

    except:
        print(f"Retrying with another proxy.")
        fetch_trending_topics()  
    finally:
        driver.quit()

    # Prepare and save the record to MongoDB
    record = {
        "_id": str(uuid.uuid4()),
        "trends": trends,
        "timestamp": datetime.now(),
        "ip_address": ip_address
    }
    print(record)
    save_to_mongo(record)



def get_latest_record():
    """Fetch the latest record based on timestamp."""
    return collection.find_one(sort=[("timestamp", -1)])

@app.route("/")
def home():
    latest_record = get_latest_record()
    trends = latest_record.get("trends", []) if latest_record else []
    return render_template("index.html", trends=trends)

@app.route("/scrape_and_fetch", methods=["GET"])
def scrape_and_fetch():
    """Run the scraping process and fetch the latest record."""
    fetch_trending_topics()
    latest_record = get_latest_record()
    return jsonify(latest_record)

if __name__ == "__main__":
    app.run(debug=True)
