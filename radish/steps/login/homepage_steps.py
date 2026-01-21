from radish import step
from pages.home_page import HomePage
from utils.allure_logger import log_step


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

@step("I open Rahul Shetty Academy homepage")
def open_homepage(step):
    log_step("Opening Rahul Shetty Academy homepage")
    page = HomePage(step.context.driver)
    page.open()

@step('page title should contain "{expected}"')
def verify_title(step, expected):
    log_step(f"Verifying page title contains: {expected}")
    page = HomePage(step.context.driver)
    page.wait_for_title_contains(expected)

    actual = page.get_title()
    log_step(f"Actual page title: {actual}")

    assert expected in actual