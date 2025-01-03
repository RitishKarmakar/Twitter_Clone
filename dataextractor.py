import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
import uuid


client = MongoClient("mongodb://localhost:27017/") 
db = client["stir_tech_intenship"]  
collection = db["trending_topics"] 




PROXY_LIST =[]
with open("valid_proxies_server.txt","r") as f:
    proxies = f.read().split("\n")
    for prox in proxies:
        PROXY_LIST.append(prox)


def get_driver(proxy):
    
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def fetch_trending_topics():
    proxy = random.choice(PROXY_LIST)
    driver = get_driver(proxy)
    try:
        driver.get("https://x.com/i/flow/login")  # Log in required
        time.sleep(4)  # Wait for the page to load
        
        email_em = driver.find_element(By.XPATH,"//input[@name='text']")
        email_em.send_keys("karmakarri80145")
        time.sleep(1)
        next_em = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
        next_em.click()
        time.sleep(3)
        # email_em = driver.find_element(By.XPATH,"//input[@name='text']")
        # email_em.send_keys("ritishinternships@gmail.com")
        # time.sleep(1)
        # next_em = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
        # next_em.click()
        # time.sleep(4)
        pass_em = driver.find_element(By.XPATH,"//input[@name='password']")
        pass_em.send_keys("..Internship@2025")
        time.sleep(1)

        login_em = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
        login_em.click()
        time.sleep(7)

        # login_em = driver.find_element(By.XPATH,LOGIN_X_PATH)
        # email_em.click()
    
        trending_elements = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")
        trends = [elem.text for elem in trending_elements[:5]]

        # Get IP address used
        ip_address = proxy
        time.sleep(7)
    except:
       print("Trying another proxy ")
       fetch_trending_topics()
    finally:
        driver.quit()

    # Prepare data for MongoDB
    record = {
        "_id": str(uuid.uuid4()),
        "trends": trends,
        "timestamp": datetime.now(),
        "ip_address": ip_address
    }
    save_to_mongo(record)
    

def save_to_mongo(record):
    collection.insert_one(record)

if __name__ == "__main__":
    fetch_trending_topics()
    # save_to_mongo(record)
    #print("Data saved:", record)
