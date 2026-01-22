import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

def get_driver():
    browser = os.getenv("BROWSER", "chrome").lower()
    remote = os.getenv("REMOTE", "false").lower() == "true"
    grid_url = os.getenv("GRID_URL", "http://localhost:4444/wd/hub")

    if browser == "edge":
        options = EdgeOptions()
    else:
        options = ChromeOptions()

    # CI / Headless
    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    # -------- Remote Grid --------
    if remote:
        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )
    else:
        if browser == "edge":
            driver = webdriver.Edge(service=EdgeService(), options=options)
        else:
            driver = webdriver.Chrome(service=ChromeService(), options=options)

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    return driver
