import allure
from radish import before

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
