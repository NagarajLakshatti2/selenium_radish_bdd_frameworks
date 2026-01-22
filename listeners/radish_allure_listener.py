# listeners/radish_allure_listener.py
from radish import after
import os
import base64

class AllureListener:
    def __init__(self):
        after.each_step(self.after_step)

    def after_step(self, step):
        driver = getattr(step.context, "driver", None)
        if driver:
            screenshots_dir = "allure-results/screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            path = os.path.join(screenshots_dir, f"{step.name.replace(' ', '_')}.png")
            driver.save_screenshot(path)

            with open(path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode("utf-8")
            step.attach(img_base64, "image/png", step.name)
