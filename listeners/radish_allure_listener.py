import allure
from radish import before, after, scenario
from datetime import datetime
import os

# Utility to capture screenshot
def capture_screenshot(driver, name="screenshot"):
    screenshots_dir = "allure-results/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    return file_path

# Before each scenario
@before.each_scenario
def before_scenario(scenario):
    allure.dynamic.title(scenario.name)

# After each step
@after.each_step
def after_step(step):
    if step.status.name == "failed":
        driver = step.context.driver
        screenshot_path = capture_screenshot(driver, step.name.replace(" ", "_"))
        allure.attach.file(screenshot_path, name=step.name, attachment_type=allure.attachment_type.PNG)

# After each scenario
@after.each_scenario
def after_scenario(scenario):
    if scenario.status.name == "failed":
        driver = scenario.context.driver
        screenshot_path = capture_screenshot(driver, scenario.name.replace(" ", "_"))
        allure.attach.file(screenshot_path, name="Scenario Failure", attachment_type=allure.attachment_type.PNG)
