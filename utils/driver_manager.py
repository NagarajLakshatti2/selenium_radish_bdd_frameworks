import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverManager:

    @staticmethod
    def get_driver():
        options = Options()

        # CI / headless support
        if os.getenv("CI") == "true":
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--start-maximized")

        return webdriver.Chrome(options=options)
