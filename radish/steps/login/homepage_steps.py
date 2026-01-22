import os

from radish import step
from webdriver_manager.core import driver

from pages.home_page import HomePage
from utils.allure_logger import log_step


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
# Ensure screenshot folder exists
os.makedirs("allure-results/screenshots", exist_ok=True)

@step("I open Rahul Shetty Academy homepage")
def open_homepage(step):
    log_step("Opening Rahul Shetty Academy homepage")
    page = HomePage(step.context.driver)
    page.open()
    # Save screenshot for this step
    # step.context.screenshot_path = "allure-results/screenshots/homepage_page.png"
    # step.context.driver.save_screenshot(step.context.screenshot_path)

@step('page title should contain "{expected}"')
def verify_title(step, expected):
    log_step(f"Verifying page title contains: {expected}")
    page = HomePage(step.context.driver)
    page.wait_for_title_contains(expected)

    actual = page.get_title()
    log_step(f"Actual page title: {actual}")

    assert expected in actual
