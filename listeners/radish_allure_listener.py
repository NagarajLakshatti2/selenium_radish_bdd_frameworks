import allure
from radish import before, after


# ---------------- Feature ----------------
@before.each_feature
def before_feature(feature):
    try:
        allure.dynamic.feature(feature.sentence)
    except Exception:
        pass


# ---------------- Scenario ----------------
@before.each_scenario
def before_scenario(scenario):
    try:
        allure.dynamic.story(scenario.sentence)
    except Exception:
        pass


@after.each_scenario
def after_scenario(scenario):
    try:
        if getattr(scenario, "state", None) == "failed":
            driver = scenario.context.driver

            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            allure.attach(
                driver.page_source,
                name="page_source",
                attachment_type=allure.attachment_type.HTML
            )
    except Exception:
        pass


# ---------------- Step ----------------
@before.each_step
def before_each_step(step):
    try:
        step._allure_ctx = allure.step(step.sentence)
        step._allure_ctx.__enter__()
    except Exception:
        pass


@after.each_step
def after_each_step(step):
    try:
        if hasattr(step, "_allure_ctx"):
            step._allure_ctx.__exit__(None, None, None)

        if getattr(step, "state", None) == "failed":
            driver = step.context.driver

            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"{step.sentence}_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            allure.attach(
                driver.page_source,
                name=f"{step.sentence}_page_source",
                attachment_type=allure.attachment_type.HTML
            )
    except Exception:
        pass
