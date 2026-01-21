from radish import given, when, then
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given("I open the login page")
def step_open_login_page(step):
    step.context.login_page = LoginPage(step.context.driver)
    step.context.login_page.open_login_page()

@when('I enter username "{username}"')
def step_enter_username(step, username):
    step.context.login_page.enter_username(username)

@when('I enter password "{password}"')
def step_enter_password(step, password):
    step.context.login_page.enter_password(password)

@when("I click on the sign in button")
def step_click_sign_in(step):
    step.context.login_page.click_sign_in()

@then("I should be logged in successfully")
def step_verify_login_success(step):
    assert step.context.login_page.is_login_successful(), "Login failed!"

@then("I should see the home page")
def step_see_home_page(step):
    assert step.context.login_page.is_home_page_displayed(), "Home page not displayed!"

@then("I should see an error message")
def step_see_error_message(step):
    assert step.context.login_page.is_error_message_displayed(), "Error message not displayed!"
