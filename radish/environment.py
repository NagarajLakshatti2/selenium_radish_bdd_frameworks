import sys
import os
import allure
from radish import before, after

# 🔑 Add project root to PYTHONPATH FIRST
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now you can safely import utils
from utils.driver_manager import DriverManager


@before.each_scenario
def start_browser(scenario):
    scenario.context.driver = DriverManager.get_driver()


@after.each_scenario
def close_browser(scenario):
    driver = scenario.context.driver

    if scenario.state == "FAILED":
        # 📸 Screenshot
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        # 📄 Page Source
        allure.attach(
            driver.page_source,
            name="Page Source",
            attachment_type=allure.attachment_type.HTML
        )

    driver.quit()
