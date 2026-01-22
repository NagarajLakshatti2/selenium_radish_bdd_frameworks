# run_tests.py
import subprocess
import sys

# This line will automatically register your before/after scenario hooks
import listeners.radish_hooks

# === RUN RADISH ===
def run_radish_command():
    print("🚀 Running Radish tests...")
    cmd = ["radish", "features/", "--junit-xml=allure-results/junit.xml"]
    subprocess.run(cmd)
    print("✅ Radish execution completed")


if __name__ == '__main__':
    run_radish_command()
    subprocess.run([sys.executable, "run_full_report.py"])