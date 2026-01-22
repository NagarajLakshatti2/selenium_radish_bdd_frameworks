import sys
import os
import allure
from radish import before, after

# 🔑 Add project root to PYTHONPATH FIRST
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now you can safely import utils
# from utils.driver_manager import DriverManager
from utils.driver_manager import get_driver



# @before.each_scenario
# def start_browser(scenario):
#     scenario.context.driver = get_driver()
#
#
# @after.each_scenario
# def close_browser(scenario):
#     driver = scenario.context.driver
#
#     if scenario.state == "FAILED":
#         # 📸 Screenshot
#         allure.attach(
#             driver.get_screenshot_as_png(),
#             name="Failure Screenshot",
#             attachment_type=allure.attachment_type.PNG
#         )
#
#         # 📄 Page Source
#         allure.attach(
#             driver.page_source,
#             name="Page Source",
#             attachment_type=allure.attachment_type.HTML
#         )
#
#     driver.quit()

@before.each_scenario
def start_browser(scenario):
    scenario.context.driver = get_driver()

@after.each_scenario
def stop_browser(scenario):
    if hasattr(scenario.context, "driver"):
        scenario.context.driver.quit()

@after.each_step
def screenshot_on_failure(step):
    driver = getattr(step.context, "driver", None)
    if driver and step.state == "failed":
        os.makedirs("allure-results/screenshots", exist_ok=True)
        path = f"allure-results/screenshots/{step.id}.png"
        driver.save_screenshot(path)