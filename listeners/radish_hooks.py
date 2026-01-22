import os
from radish import before, after

SCREENSHOT_FOLDER = "screenshots"
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)


def sanitize_filename(name):
    return (
        name.replace(" ", "_")
            .replace('"', "")
            .replace("/", "_")
            .lower()
    )


@before.each_scenario
def before_scenario(scenario):
    try:
        if hasattr(scenario.context, "driver"):
            filename = os.path.join(
                SCREENSHOT_FOLDER,
                f"{sanitize_filename(scenario.sentence)}_start.png"
            )
            scenario.context.driver.save_screenshot(filename)
    except Exception:
        # ⚠️ hooks must never crash
        pass


@after.each_scenario
def after_scenario(scenario):
    try:
        if hasattr(scenario.context, "driver"):
            filename = os.path.join(
                SCREENSHOT_FOLDER,
                f"{sanitize_filename(scenario.sentence)}_end.png"
            )
            scenario.context.driver.save_screenshot(filename)
    except Exception:
        # ⚠️ hooks must never crash
        pass
