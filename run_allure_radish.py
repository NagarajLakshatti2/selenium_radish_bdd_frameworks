import subprocess
import sys
import os

# Paths
FEATURES_DIR = "features"
ALLURE_RESULTS = "allure-results"
ALLURE_REPORT = "allure-report"

def run_radish_tests():
    print("=== Running Radish tests ===")
    # Ensure allure-results folder exists
    os.makedirs(ALLURE_RESULTS, exist_ok=True)

    # cmd = [
    #     "radish",
    #     FEATURES_DIR,
    #     f"--junit-xml={ALLURE_RESULTS}/junit.xml"
    # ]

    cmd = [
        sys.executable,
        "-c",
        (
            "import listeners.radish_hooks;"
            "from radish import main;"
            f"main.main(['{FEATURES_DIR}', '--junit-xml={ALLURE_RESULTS}/junit.xml'])"
        )
    ]

    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Radish tests failed or did not run. Exiting.")
        sys.exit(1)
    print("Radish tests completed successfully.\n")

    # result = subprocess.run(cmd)
    # if result.returncode != 0:
    #     sys.exit(1)

def generate_allure_report():
    print("=== Generating Allure report ===")
    cmd = f"allure generate {ALLURE_RESULTS} --clean -o {ALLURE_REPORT}"
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Failed to generate Allure report. Exiting.")
        sys.exit(1)
    # print("Allure report generated successfully.\n")
    # subprocess.run(
    #     ["allure", "generate", ALLURE_RESULTS, "--clean", "-o", ALLURE_REPORT],
    #     shell=True,
    #     check=True
    # )

def open_allure_report():
    print("=== Opening Allure report ===")
    cmd = f"allure open {ALLURE_REPORT}"
    subprocess.run(cmd, shell=True)
    # print("=== Opening Allure report ===")
    # subprocess.run(
    #     f"allure open {ALLURE_REPORT}",
    #     shell=True
    # )

if __name__ == "__main__":
    run_radish_tests()
    generate_allure_report()
    open_allure_report()



