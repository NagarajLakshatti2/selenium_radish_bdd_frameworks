from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://rahulshettyacademy.com/loginpagePractise/"

    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SIGNIN_BUTTON = (By.ID, "signInBtn")
    HOME_PAGE_HEADER = (By.XPATH, "//h2[contains(text(),'Welcome')]")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='alert-danger']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open_login_page(self):
        self.driver.get(self.LOGIN_URL)

    def enter_username(self, username):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT)).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_sign_in(self):
        self.wait.until(EC.element_to_be_clickable(self.SIGNIN_BUTTON)).click()

    def is_login_successful(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.HOME_PAGE_HEADER))
            return True
        except:
            return False

    def is_home_page_displayed(self):
        return self.is_login_successful()

    def is_error_message_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except:
            return False
