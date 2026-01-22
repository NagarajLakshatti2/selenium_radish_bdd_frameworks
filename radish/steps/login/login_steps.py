import os

from radish import step

from pages.login_page import LoginPage

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Ensure screenshot folder exists
os.makedirs("allure-results/screenshots", exist_ok=True)

@step("I open the login page")
def step_open_login_page(step):
    step.context.login_page = LoginPage(step.context.driver)
    step.context.login_page.open_login_page()
    # Save screenshot for this step


@step('I enter username "{username}"')
def step_enter_username(step, username):
    step.context.login_page.enter_username(username)

@step('I enter password "{password}"')
def step_enter_password(step, password):
    step.context.login_page.enter_password(password)

@step("I click on the sign in button")
def step_click_sign_in(step):
    step.context.login_page.click_sign_in()

@step("I should be logged in successfully")
def step_verify_login_success(step):
    assert step.context.login_page.is_login_successful(), "Login failed!"

@step("I should see the home page")
def step_see_home_page(step):
    assert step.context.login_page.is_home_page_displayed(), "Home page not displayed!"

@step("I should see an error message")
def step_see_error_message(step):
    assert step.context.login_page.is_error_message_displayed(), "Error message not displayed!"
