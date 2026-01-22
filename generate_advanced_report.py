import os
import json
import base64
import webbrowser
from jinja2 import Environment, FileSystemLoader

REPORT_DIR = "reports"
JSON_FILE = os.path.join(REPORT_DIR, "cucumber.json")
HTML_FILE = os.path.join(REPORT_DIR, "index.html")

def main():
    # Load Radish JSON
    if not os.path.exists(JSON_FILE):
        print(f"❌ JSON file not found: {JSON_FILE}")
        return

    with open(JSON_FILE, encoding="utf-8") as f:
        data = json.load(f)

    # Mark scenario failed or passed
    for feature in data:
        for scenario in feature.get("elements", []):
            scenario["has_failed"] = any(step["result"]["status"] == "failed" for step in scenario.get("steps", []))

    # Summary
    summary = {
        "features": len(data),
        "scenarios": sum(len(f.get("elements", [])) for f in data),
        "steps": sum(len(s.get("steps", [])) for f in data for s in f.get("elements", [])),
        "passed": sum(1 for f in data for s in f.get("elements", []) for step in s.get("steps", []) if step["result"]["status"] == "passed"),
        "failed": sum(1 for f in data for s in f.get("elements", []) for step in s.get("steps", []) if step["result"]["status"] == "failed"),
    }

    # Embed screenshots as base64
    for feature in data:
        for scenario in feature.get("elements", []):
            for step in scenario.get("steps", []):
                screenshot_path = step.get("context", {}).get("screenshot")
                if screenshot_path and os.path.exists(screenshot_path):
                    with open(screenshot_path, "rb") as img_f:
                        encoded = base64.b64encode(img_f.read()).decode("utf-8")
                        step["screenshot_base64"] = encoded

    # Jinja2 template
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Advanced Radish Selenium Report</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { padding:20px; }
.step img { max-width:300px; margin:5px 0; display:none; position:absolute; z-index:1000; border:1px solid #ccc; }
.step:hover img { display:block; }
.feature { margin-bottom:30px; }
.scenario { margin-left:20px; margin-bottom:15px; }
.step { margin-left:40px; position:relative; }
.badge-passed { background-color:#28a745; }
.badge-failed { background-color:#dc3545; }
.summary .card { margin-bottom:20px; text-align:center; }
.filter-btn { margin-right:5px; }
.collapse-button { cursor:pointer; }
</style>
</head>
<body>
<div class="container">
<h1>Advanced Radish Selenium Report</h1>

<!-- Summary -->
<div class="row summary mb-3">
  <div class="col"><div class="card"><div class="card-body"><h5>Features</h5><span class="badge bg-primary">{{ summary.features }}</span></div></div></div>
  <div class="col"><div class="card"><div class="card-body"><h5>Scenarios</h5><span class="badge bg-primary">{{ summary.scenarios }}</span></div></div></div>
  <div class="col"><div class="card"><div class="card-body"><h5>Steps</h5><span class="badge bg-primary">{{ summary.steps }}</span></div></div></div>
  <div class="col"><div class="card"><div class="card-body"><h5>Passed</h5><span class="badge badge-passed">{{ summary.passed }}</span></div></div></div>
  <div class="col"><div class="card"><div class="card-body"><h5>Failed</h5><span class="badge badge-failed">{{ summary.failed }}</span></div></div></div>
</div>

<!-- Filter Buttons -->
<div class="mb-3">
  <button class="btn btn-sm btn-success filter-btn" onclick="filterSteps('passed')">Show Passed</button>
  <button class="btn btn-sm btn-danger filter-btn" onclick="filterSteps('failed')">Show Failed</button>
  <button class="btn btn-sm btn-primary filter-btn" onclick="filterSteps('all')">Show All</button>
</div>

<!-- Features -->
{% for f_idx, feature in enumerate(data) %}
<div class="feature">
<h2>Feature: {{ feature.name }}</h2>
{% for s_idx, scenario in enumerate(feature.elements) %}
<div class="scenario">
<h4 class="collapse-button" data-bs-toggle="collapse" href="#scenario-{{ f_idx }}-{{ s_idx }}">
Scenario: {{ scenario.name }}
<span class="badge {% if scenario.has_failed %}badge-failed{% else %}badge-passed{% endif %}">
{% if scenario.has_failed %}Failed{% else %}Passed{% endif %}
</span>
</h4>
<div class="collapse show" id="scenario-{{ f_idx }}-{{ s_idx }}">
  {% for step in scenario.steps %}
  <div class="step {{ step.result.status }}">
    {{ step.keyword }} {{ step.name }} — 
    <span class="badge {% if step.result.status == 'passed' %}badge-passed{% else %}badge-failed{% endif %}">{{ step.result.status }}</span>
    {% if step.screenshot_base64 %}
      <img src="data:image/png;base64,{{ step.screenshot_base64 }}">
    {% endif %}
  </div>
  {% endfor %}
</div>
</div>
{% endfor %}
</div>
{% endfor %}

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
function filterSteps(status) {
  document.querySelectorAll('.step').forEach(function(step){
    if(status === 'all'){
      step.style.display = 'block';
    } else {
      step.style.display = step.classList.contains(status) ? 'block' : 'none';
    }
  });
}
</script>
</body>
</html>
""")

    html_content = template.render(data=data, summary=summary, enumerate=enumerate)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Advanced report generated: {HTML_FILE}")
    webbrowser.open_new_tab(os.path.abspath(HTML_FILE))


if __name__ == "__main__":
    main()
