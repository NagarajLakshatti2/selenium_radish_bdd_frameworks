
from pages.base_page import BasePage

class HomePage(BasePage):

    URL = "https://rahulshettyacademy.com/"

    def open(self):
        self.driver.get(self.URL)
