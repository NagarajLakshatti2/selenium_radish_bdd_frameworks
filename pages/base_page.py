from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_title_contains(self, text):
        self.wait.until(EC.title_contains(text))

    def get_title(self):
        return self.driver.title
