from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
import uuid

# Configure MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_scraper']
collection = db['trending_topics']

# Configure Selenium with ProxyMesh
proxy = "your-proxymesh-username:your-proxymesh-password@proxy-ip:port"
chrome_options = Options()
chrome_options.add_argument(f"--proxy-server=http://{proxy}")

service = Service('path/to/chromedriver')  # Add your ChromeDriver path here
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_trending_topics():
    try:
        # Log in to Twitter
        driver.get("https://twitter.com/login")
        driver.implicitly_wait(10)

        # Enter your credentials
        username = driver.find_element(By.NAME, "session[username_or_email]")
        password = driver.find_element(By.NAME, "session[password]")
        username.send_keys("your_twitter_username")
        password.send_keys("your_twitter_password")
        password.send_keys(Keys.RETURN)

        # Navigate to the home page
        driver.implicitly_wait(10)
        driver.get("https://twitter.com/home")

        # Fetch trending topics
        trending_topics = driver.find_elements(By.CSS_SELECTOR, "section[aria-labelledby] div div div span")[:5]
        trends = [topic.text for topic in trending_topics if topic.text]

        # Store results in MongoDB
        unique_id = str(uuid.uuid4())
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = proxy.split('@')[-1].split(':')[0]

        data = {
            "_id": unique_id,
            "trend1": trends[0] if len(trends) > 0 else "",
            "trend2": trends[1] if len(trends) > 1 else "",
            "trend3": trends[2] if len(trends) > 2 else "",
            "trend4": trends[3] if len(trends) > 3 else "",
            "trend5": trends[4] if len(trends) > 4 else "",
            "end_time": end_time,
            "ip_address": ip_address
        }
        collection.insert_one(data)

        return data
    finally:
        driver.quit()