from radish import before
import os

@before.all
def write_allure_environment(features):
    os.makedirs("allure-results", exist_ok=True)

    with open("allure-results/environment.properties", "w") as f:
        f.write(f"Browser={os.getenv('BROWSER', 'chrome')}\n")
        f.write("Framework=Radish BDD + Selenium\n")
        f.write(f"CI={os.getenv('CI', 'false')}\n")
        f.write(f"GridURL={os.getenv('GRID_URL', 'local')}\n")
