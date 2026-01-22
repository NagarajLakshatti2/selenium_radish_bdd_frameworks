import os
import json
import subprocess
import sys
import webbrowser

from jinja2 import Template
from datetime import datetime

# === CONFIGURATION ===
RADISH_JSON_PATH = "allure-results/radish_results.json"
OUTPUT_HTML_PATH = "allure-report/index.html"
SCREENSHOT_FOLDER = "screenshots"
INCLUDE_PASS_SCREENSHOT = True  # Set False if you don't want screenshots for passed steps

# === UTILS ===
def load_results(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_step_badge(step):
    return {"passed":"✅","failed":"❌","skipped":"⚠"}.get(step.get("result", {}).get("status"), "❔")

def find_screenshots(step_name):
    base_name = step_name.replace(" ", "_").lower()
    before = os.path.join(SCREENSHOT_FOLDER, f"{base_name}_before.png")
    after = os.path.join(SCREENSHOT_FOLDER, f"{base_name}_after.png")
    return (before if os.path.exists(before) else None,
            after if os.path.exists(after) else None)


# === REPORT GENERATION ===
def generate_report(data):
    TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BDD Test Report</title>
<link href="https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.min.css" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.umd.min.js"></script>
<style>
body { font-family: Arial, sans-serif; margin:0; display:flex; height:100vh; }
.sidebar { width:250px; background:#2f3e46; color:white; overflow:auto; padding:15px; }
.sidebar h2 { font-size:18px; margin-top:0; }
.sidebar ul { list-style:none; padding-left:0; }
.sidebar li { cursor:pointer; padding:5px; }
.sidebar li:hover { background:#354f52; }
.sidebar li.collapsed::before { content: '▶ '; }
.sidebar li.expanded::before { content: '▼ '; }
.main { flex:1; overflow:auto; padding:20px; background:#f0f0f0; }
.card { background:white; padding:15px; margin-bottom:15px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);}
.card[data-status="passed"] { border-left:4px solid #4caf50; }
.card[data-status="failed"] { border-left:4px solid #f44336; }
.card[data-status="skipped"] { border-left:4px solid #ff9800; }
.step { padding:5px 0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; position:relative; }
.step img { max-height:60px; margin-left:10px; border:1px solid #ccc; border-radius:4px; margin-top:5px;}
.step .tooltip { visibility:hidden; background:rgba(0,0,0,0.8); color:white; text-align:left; padding:5px; border-radius:4px; position:absolute; z-index:10; top:25px; left:0; font-size:12px; max-width:250px; }
.step:hover .tooltip { visibility:visible; }
h3 { margin-top:0; }
.slider-container { margin-top:10px; }
.filter-btn { cursor:pointer; padding:5px 10px; background:#52796f; margin:2px; display:inline-block; border-radius:4px; font-size:12px; }
.filter-btn:hover { background:#354f52; }
.charts-container { display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px; margin-bottom:20px; }
.chart-box { flex:1; min-width:300px; max-width:400px; background:white; padding:10px; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1);}
.summary-container { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-bottom:20px; }
.summary-box { flex:1; min-width:200px; background:#fff; padding:10px; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); margin:5px; text-align:center; }
</style>
</head>
<body>
<div class="sidebar">
  <h2>Filters</h2>
  <div>
      <span class="filter-btn" onclick="filterCards('all')">All</span>
      <span class="filter-btn" onclick="filterCards('passed')">Passed</span>
      <span class="filter-btn" onclick="filterCards('failed')">Failed</span>
      <span class="filter-btn" onclick="filterCards('skipped')">Skipped</span>
  </div>
  <h2>Features</h2>
  <ul>
  {% for feature in data %}
      <li class="feature collapsed">
          <span class="feature-title" onclick="toggleFeature('{{loop.index0}}')">{{feature['name']}}</span>
          <ul class="scenario-list" id="feature-{{loop.index0}}" style="display:none;">
          {% for scenario in feature['scenarios'] %}
              <li class="scenario {% if scenario.status=='passed' %}collapsed{% else %}expanded{% endif %}" 
                  onclick="scrollToScenario('scenario-{{feature['name']}}-{{loop.index0}}', event)">
                  {{scenario['name']}}
              </li>
          {% endfor %}
          </ul>
      </li>
  {% endfor %}
  </ul>
</div>

<div class="main">
<h2>BDD Test Report</h2>
<div style="margin-bottom:15px;">
    <input type="text" id="searchBox" placeholder="Search features or scenarios..." 
        style="width:100%; padding:8px; border-radius:5px; border:1px solid #ccc; font-size:14px;">
</div>

<div class="summary-container">
  <div class="summary-box">
    <h3>Total Features</h3>
    <p id="total-features">0</p>
  </div>
  <div class="summary-box">
    <h3>Total Scenarios</h3>
    <p id="total-scenarios">0</p>
  </div>
  <div class="summary-box">
    <h3>Total Steps</h3>
    <p id="total-steps">0</p>
  </div>
  <div class="chart-box">
    <canvas id="summaryChart" height="150"></canvas>
  </div>
</div>

<div class="charts-container">
  <div class="chart-box"><canvas id="overallChart" height="200"></canvas></div>
  <div class="chart-box"><canvas id="scenarioChart" height="200"></canvas></div>
</div>

{% for feature in data %}
    <h2>{{feature['name']}}</h2>
    {% for scenario in feature['scenarios'] %}
    <div class="card" id="scenario-{{feature['name']}}-{{loop.index0}}" data-status="{{scenario.status}}">
        <h3>{{scenario['name']}}</h3>
        {% for step in scenario['steps'] %}
        <div class="step">
            <span>{{get_step_badge(step)}} {{step['name']}}</span>
            <div class="tooltip">
                Status: {{step.result.status}}<br>
                {% if step.result.error_message %}Error: {{step.result.error_message}}<br>{% endif %}
                Time: {{step.timestamp}}
            </div>
            {% if step.screenshot_before or step.screenshot_after %}
            <div class="slider-container" id="slider-{{feature['name']}}-{{loop.index0}}-{{loop.index0}}"></div>
            <script>
            window.addEventListener('load', function() {
                var slider = document.getElementById('slider-{{feature['name']}}-{{loop.index0}}-{{loop.index0}}');
                if(slider && !slider.hasChildNodes()){
                    var container = document.createElement('div');
                    container.style.position = 'relative';
                    container.style.width = '200px';
                    container.style.height = '60px';
                    {% if step.screenshot_before %}
                    var before = document.createElement('img');
                    before.src = '{{step.screenshot_before}}';
                    before.style.width='100%';
                    before.style.position='absolute';
                    container.appendChild(before);
                    {% endif %}
                    {% if step.screenshot_after %}
                    var after = document.createElement('img');
                    after.src = '{{step.screenshot_after}}';
                    after.style.width='100%';
                    after.style.position='absolute';
                    after.style.clip='rect(0px, 100%, 60px, 0px)';
                    container.appendChild(after);

                    var range = document.createElement('input');
                    range.type='range'; range.min=0; range.max=200; range.value=100;
                    range.style.width='100%';
                    range.oninput = function(){ 
                        after.style.clip = 'rect(0px,'+this.value+'px,60px,0px)'; 
                    }
                    container.appendChild(range);
                    {% endif %}
                    slider.appendChild(container);
                }
            });
            </script>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% endfor %}
{% endfor %}
</div>

<script>
// === Sidebar & Scroll ===
function toggleFeature(idx){
    var ul = document.getElementById('feature-'+idx);
    var featureLi = ul.parentElement;
    if(ul.style.display=='none'){ ul.style.display='block'; featureLi.classList.remove('collapsed'); featureLi.classList.add('expanded'); }
    else{ ul.style.display='none'; featureLi.classList.remove('expanded'); featureLi.classList.add('collapsed'); }
}
function scrollToScenario(id, event){ if(event) event.stopPropagation(); document.getElementById(id).scrollIntoView({behavior:'smooth'}); }
window.addEventListener('load', function(){
    document.querySelectorAll('.scenario-list').forEach(list=>{
        list.querySelectorAll('li.scenario.collapsed').forEach(s=>{ s.style.display='none'; });
    });
});

// === Charts & Filters ===
var allCards = {{ data | safe }};
function getChartData(status){
    var passed=0, failed=0, skipped=0; var labels=[], pData=[], fData=[], sData=[];
    allCards.forEach(f=>{ f.scenarios.forEach(s=>{
        if(status==='all'||s.status===status){ labels.push(s.name); pData.push(s.passed_steps); fData.push(s.failed_steps); sData.push(s.skipped_steps); }
        passed+=s.passed_steps; failed+=s.failed_steps; skipped+=s.skipped_steps;
    })});
    return {labels,pData,fData,sData,passed,failed,skipped};
}

function computeTotals(){
    var totalFeatures=allCards.length,totalScenarios=0,totalSteps=0,passed=0,failed=0,skipped=0;
    allCards.forEach(f=>{ totalScenarios+=f.scenarios.length; f.scenarios.forEach(s=>{
        totalSteps+=s.passed_steps+s.failed_steps+s.skipped_steps;
        passed+=s.passed_steps; failed+=s.failed_steps; skipped+=s.skipped_steps;
    })});
    document.getElementById('total-features').innerText=totalFeatures;
    document.getElementById('total-scenarios').innerText=totalScenarios;
    document.getElementById('total-steps').innerText=totalSteps;
    return {passed,failed,skipped};
}

var totals = computeTotals();
var summaryCtx = document.getElementById('summaryChart').getContext('2d');
var summaryChart = new Chart(summaryCtx,{
    type:'doughnut',
    data:{labels:['Passed','Failed','Skipped'], datasets:[{data:[totals.passed,totals.failed,totals.skipped], backgroundColor:['#4caf50','#f44336','#ff9800']}]},
    options:{responsive:true, plugins:{legend:{position:'bottom'}}, onClick:function(evt,items){ if(items.length>0){ filterCards(this.data.labels[items[0].index].toLowerCase()); }} }
});

var overallCtx = document.getElementById('overallChart').getContext('2d');
var scenarioCtx = document.getElementById('scenarioChart').getContext('2d');
var chartData = getChartData('all');
var overallChart = new Chart(overallCtx,{ type:'doughnut', data:{labels:['Passed','Failed','Skipped'], datasets:[{data:[chartData.passed,chartData.failed,chartData.skipped], backgroundColor:['#4caf50','#f44336','#ff9800']}]}, options:{responsive:true, plugins:{legend:{position:'bottom'}}, onClick:function(evt,items){ if(items.length>0){ filterCards(this.data.labels[items[0].index].toLowerCase()); }} } });
var scenarioChart = new Chart(scenarioCtx,{ type:'bar', data:{labels:chartData.labels, datasets:[{label:'Passed',data:chartData.pData,backgroundColor:'#4caf50'}, {label:'Failed',data:chartData.fData,backgroundColor:'#f44336'}, {label:'Skipped',data:chartData.sData,backgroundColor:'#ff9800'}]}, options:{responsive:true, plugins:{legend:{position:'bottom'}}, scales:{x:{stacked:true}, y:{stacked:true}}, onClick:function(evt,items){ if(items.length>0){ var index=items[0].index; var scenarioName=this.data.labels[index]; var cardId=null; allCards.forEach(f=>{ f.scenarios.forEach((s,i)=>{ if(s.name===scenarioName) cardId='scenario-'+f.name+'-'+i; });}); if(cardId) scrollToScenario(cardId); } } } });

function updateCharts(filterStatus){ 
    var data=getChartData(filterStatus); 
    overallChart.data.datasets[0].data=[data.passed,data.failed,data.skipped]; overallChart.update();
    scenarioChart.data.labels=data.labels; scenarioChart.data.datasets[0].data=data.pData; scenarioChart.data.datasets[1].data=data.fData; scenarioChart.data.datasets[2].data=data.sData; scenarioChart.update(); 
}
function filterCards(status){
    var cards=document.querySelectorAll('.card'); cards.forEach(c=>{ c.style.display=(status==='all'||c.getAttribute('data-status')===status)?'block':'none'; });
    document.querySelectorAll('.scenario-list').forEach(list=>{ list.querySelectorAll('li.scenario').forEach(s=>{
        s.style.display=(status==='failed')? (s.classList.contains('expanded')?'block':'none'):'block';
    })});
    updateCharts(status);
}

document.getElementById('searchBox').addEventListener('input', function(){
    var query = this.value.toLowerCase();
    document.querySelectorAll('.card').forEach(card=>{
        var scenarioName = card.querySelector('h3').innerText.toLowerCase();
        var featureName = card.id.split('-')[1].toLowerCase();
        card.style.display = (scenarioName.includes(query) || featureName.includes(query)) ? 'block' : 'none';
    });
});
</script>
</body>
</html>
"""
    template = Template(TEMPLATE_HTML)
    return template.render(data=data, get_step_badge=get_step_badge)

# === MAIN ===
if __name__ == "__main__":
    raw = load_results(RADISH_JSON_PATH)
    features = []
    for feature_json in raw:
        feature = {"name": feature_json.get("name"), "scenarios": []}
        for scenario_json in feature_json.get("elements", []):
            if scenario_json.get("type")!="scenario": continue
            scenario = {"name": scenario_json.get("name"), "steps":[], "passed_steps":0,"failed_steps":0,"skipped_steps":0}
            scenario_status="passed"
            for step_json in scenario_json.get("steps", []):
                status = step_json.get("result", {}).get("status")
                if status=="failed": scenario_status="failed"
                elif status=="skipped" and scenario_status!="failed": scenario_status="skipped"
            scenario["status"]=scenario_status
            for step_json in scenario_json.get("steps", []):
                step_name = step_json.get("name")
                before, after = find_screenshots(step_name)
                if step_json.get("result", {}).get("status")=="passed" and not INCLUDE_PASS_SCREENSHOT: before=after=None
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                step = {"name":step_name,
                        "result":{"status":step_json.get("result",{}).get("status"),
                                  "error_message":step_json.get("result",{}).get("error_message")},
                        "screenshot_before":before,
                        "screenshot_after":after,
                        "timestamp":timestamp}
                if step["result"]["status"]=="passed": scenario["passed_steps"]+=1
                elif step["result"]["status"]=="failed": scenario["failed_steps"]+=1
                elif step["result"]["status"]=="skipped": scenario["skipped_steps"]+=1
                scenario["steps"].append(step)
            feature["scenarios"].append(scenario)
        features.append(feature)

    os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
    html = generate_report(features)
    with open(OUTPUT_HTML_PATH,"w",encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Modern Allure-style report generated at {OUTPUT_HTML_PATH}")

    # === Auto open in default browser ===
    abs_path = os.path.abspath(OUTPUT_HTML_PATH)
    webbrowser.open(f"file:///{abs_path}")
    print(f"🌐 Opening report in browser: {abs_path}")
