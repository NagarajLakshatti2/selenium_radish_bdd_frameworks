# listeners/radish_hooks.py
import datetime
import shutil

from radish import before, after
import os
import base64
import allure

class RadishHooks():
    def __init__(self):
        pass
# ------------------------------
# 1️⃣ Write Allure environment
# ------------------------------
@before.all
def write_allure_environment(features):
    allure_dir = "allure-results"

    # 🔥 Clean old results
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)

    # ✅ Recreate folder
    os.makedirs(allure_dir, exist_ok=True)

    # 🕒 Current date & time
    run_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    build_number = (
            os.getenv("GITHUB_RUN_NUMBER") or
            os.getenv("BUILD_NUMBER") or
            os.getenv("BUILD_BUILDNUMBER") or
            os.getenv("CI_PIPELINE_ID") or
            "LOCAL"
    )

    with open("allure-results/environment.properties", "w") as f:
        f.write(f"Author={os.getenv('Author', 'Nagaraj Lakshatti')}\n")
        f.write(f"Browser={os.getenv('BROWSER', 'chrome')}\n")
        f.write("Framework=Radish BDD + Selenium\n")
        f.write(f"CI={os.getenv('CI', 'false')}\n")
        f.write(f"GridURL={os.getenv('GRID_URL', 'local')}\n")
        f.write(f"DD-MM-YY H:M:S= {run_time}\n")
        f.write(f"Build_Number={build_number}\n")

# ------------------------------
# 2️⃣ Apply Allure labels based on scenario tags
# ------------------------------
@before.each_scenario
def apply_allure_labels(scenario):
    for tag in scenario.tags:
        tag_lower = tag.lower()

        # Map common tags to severity
        if tag_lower == "smoke":
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        elif tag_lower == "regression":
            allure.dynamic.severity(allure.severity_level.NORMAL)
        elif tag_lower == "sanity":
            allure.dynamic.severity(allure.severity_level.MINOR)

        # Add all tags to Allure
        allure.dynamic.tag(tag)

# ------------------------------
# 3️⃣ Attach screenshot after each step
# ------------------------------
@after.each_step
def attach_screenshot(step):
    driver = getattr(step.context, "driver", None)
    if driver:
        screenshots_dir = "allure-results/screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        safe_name = step.name.replace(" ", "_")
        path = os.path.join(screenshots_dir, f"{safe_name}.png")

        driver.save_screenshot(path)

        with open(path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")
        step.attach(img_base64, "image/png", step.name)

@after.each_step
def attach_screenshot_on_failure(step):
    driver = getattr(step.context, "driver", None)

    if not driver or step.state != "failed":
        return

    # 📂 Ensure screenshots folder
    screenshot_dir = "allure-results/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    # 🕒 Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 🧾 Clean step name
    step_name = step.sentence.replace(" ", "_").replace("/", "_")

    # 📸 Screenshot path
    screenshot_path = f"{screenshot_dir}/{step_name}_{timestamp}.png"

    # Save screenshot
    driver.save_screenshot(screenshot_path)

    # 📎 Attach to Allure
    with open(screenshot_path, "rb") as image:
        allure.attach(
            image.read(),
            name=f"{step.sentence} ({timestamp})",
            attachment_type=allure.attachment_type.PNG
        )

# ------------------------------
# 4️⃣ Retry failed scenarios
# ------------------------------
MAX_RETRIES = int(os.getenv("RADISH_RETRIES", "1"))

@after.each_scenario
def retry_failed_scenario(scenario):
    if not scenario.failed:
        return

    # Track retries on scenario context
    retries = getattr(scenario.context, "retries", 0)

    if retries < MAX_RETRIES:
        scenario.context.retries = retries + 1
        # Mark scenario to be re-executed
        scenario.state = scenario.State.UNTESTED

# Register the listener
RadishHooks()