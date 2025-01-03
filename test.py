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

PATH = "C:\Windows\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://twitter.com/login")

time.sleep(3)
username  = driver.find_element(By.XPATH,"//input[@name='test']")
