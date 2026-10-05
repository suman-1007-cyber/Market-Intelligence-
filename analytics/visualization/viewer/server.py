import json
import html
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]


def load_data():
    candidates = [
        ROOT / "storage/gold/pipeline_11_20.json",
        ROOT / "storage/gold/pipeline_1_10.json",
    ]

    for path in candidates:
        if path.exists():
            try:
                return json.loads(path.read_text())
            except Exception:
                pass

    return {
        "status": "NO_GOLD_DATA",
        "message": "No Gold analytics output was found yet."
    }


def flatten(obj, prefix=""):
    rows = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            name = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                rows.extend(flatten(value, name))
            else:
                rows.append((name, value))

    elif isinstance(obj, list):
        for index, value in enumerate(obj[:500]):
            name = f"{prefix}[{index}]"
            if isinstance(value, (dict, list)):
                rows.extend(flatten(value, name))
            else:
                rows.append((name, value))

    return rows


def page():
    data = load_data()
    safe_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Market Intelligence Viewer</title>
<style>
*{{box-sizing:border-box}}
body{{
    margin:0;
    font-family:Arial,sans-serif;
    background:#101318;
    color:#e8edf3;
}}
header{{
    padding:22px;
    background:#171b22;
    border-bottom:1px solid #303640;
}}
h1{{margin:0 0 6px;font-size:24px}}
.subtitle{{color:#9da7b5}}
nav{{
    display:flex;
    gap:8px;
    flex-wrap:wrap;
    padding:12px 22px;
    background:#141820;
    border-bottom:1px solid #303640;
}}
button{{
    border:1px solid #3b4450;
    background:#202630;
    color:#e8edf3;
    padding:10px 14px;
    border-radius:7px;
    cursor:pointer;
}}
button:hover{{background:#2a313c}}
main{{padding:20px;max-width:1200px;margin:auto}}
.panel{{
    background:#171b22;
    border:1px solid #303640;
    border-radius:10px;
    padding:18px;
    margin-bottom:16px;
}}
.grid{{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
    gap:12px;
}}
.kpi{{
    background:#202630;
    padding:16px;
    border-radius:8px;
}}
.kpi .label{{color:#9da7b5;font-size:13px}}
.kpi .value{{font-size:24px;font-weight:bold;margin-top:5px}}
table{{width:100%;border-collapse:collapse}}
th,td{{padding:9px;border-bottom:1px solid #303640;text-align:left;vertical-align:top}}
th{{color:#aeb8c5}}
pre{{
    white-space:pre-wrap;
    word-break:break-word;
    color:#cbd5e1;
}}
svg{{width:100%;height:360px;background:#11151b;border-radius:8px}}
.small{{font-size:13px;color:#9da7b5}}
.badge{{
    display:inline-block;
    padding:5px 9px;
    border-radius:12px;
    background:#27303b;
    margin:3px;
}}
#status{{color:#9da7b5}}
</style>
</head>
<body>
<header>
<h1>Market Intelligence Viewer</h1>
<div class="subtitle">Charts • Graphs • Tables • Evidence • Analytics</div>
</header>

<nav>
<button onclick="show('overview')">Overview</button>
<button onclick="show('visual')">Visualization</button>
<button onclick="show('table')">Data Table</button>
<button onclick="show('json')">Raw Data</button>
</nav>

<main>
<section id="overview" class="view">
<div class="panel">
<h2>Analytics Overview</h2>
<div id="kpis" class="grid"></div>
</div>
<div class="panel">
<h2>Engine Status</h2>
<div id="status"></div>
</div>
</section>

<section id="visual" class="view" style="display:none">
<div class="panel">
<h2>Visualization</h2>
<div id="visualInfo"></div>
<div id="chart"></div>
</div>
</section>

<section id="table" class="view" style="display:none">
<div class="panel">
<h2>Data / Evidence Table</h2>
<div id="tableData"></div>
</div>
</section>

<section id="json" class="view" style="display:none">
<div class="panel">
<h2>Raw Analytics Output</h2>
<pre id="raw"></pre>
</div>
</section>
</main>

<script>
const DATA = {safe_json};

function allNumbers(obj) {{
    const result=[];
    function walk(x) {{
        if (typeof x === "number" && Number.isFinite(x)) result.push(x);
        else if (Array.isArray(x)) x.forEach(walk);
        else if (x && typeof x === "object") Object.values(x).forEach(walk);
    }}
    walk(obj);
    return result;
}}

function countLeaves(obj) {{
    let count=0;
    function walk(x) {{
        if (Array.isArray(x)) x.forEach(walk);
        else if (x && typeof x === "object") Object.values(x).forEach(walk);
        else count++;
    }}
    walk(obj);
    return count;
}}

function escapeHTML(x) {{
    return String(x ?? "")
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll('"',"&quot;");
}}

function show(id) {{
    document.querySelectorAll(".view").forEach(x=>x.style.display="none");
    document.getElementById(id).style.display="block";
}}

function buildTable() {{
    const rows=[];
    function walk(obj,path) {{
        if (Array.isArray(obj)) {{
            obj.slice(0,100).forEach((v,i)=>walk(v,path+"["+i+"]"));
        }} else if (obj && typeof obj==="object") {{
            Object.entries(obj).forEach(([k,v])=>walk(v,path ? path+"."+k : k));
        }} else {{
            rows.push([path,obj]);
        }}
    }}
    walk(DATA,"");

    let out="<table><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>";
    rows.slice(0,500).forEach(r=>{{
        out+="<tr><td>"+escapeHTML(r[0])+"</td><td>"+escapeHTML(r[1])+"</td></tr>";
    }});
    out+="</tbody></table>";
    document.getElementById("tableData").innerHTML=out;
}}

function drawChart() {{
    const numbers=allNumbers(DATA).slice(0,20);
    const container=document.getElementById("chart");

    if (numbers.length < 2) {{
        container.innerHTML="<p class='small'>Not enough numeric observations for a chart yet. Use the Data Table or Raw Data view.</p>";
        return;
    }}

    const W=900,H=330,P=45;
    const max=Math.max(...numbers);
    const min=Math.min(...numbers);
    const span=max-min || 1;

    const points=numbers.map((v,i)=>{{
        const x=P+i*((W-2*P)/Math.max(1,numbers.length-1));
        const y=H-P-((v-min)/span)*(H-2*P);
        return [x,y,v];
    }});

    const poly=points.map(p=>p[0]+","+p[1]).join(" ");

    let svg=`<svg viewBox="0 0 ${{W}} ${{H}}" role="img" aria-label="Analytics numeric observation plot">
        <line x1="${{P}}" y1="${{H-P}}" x2="${{W-P}}" y2="${{H-P}}" stroke="#667085"/>
        <line x1="${{P}}" y1="${{P}}" x2="${{P}}" y2="${{H-P}}" stroke="#667085"/>
        <polyline points="${{poly}}" fill="none" stroke="#8ab4f8" stroke-width="3"/>`;

    points.forEach((p,i)=>{{
        svg+=`<circle cx="${{p[0]}}" cy="${{p[1]}}" r="5" fill="#8ab4f8">
        <title>Observation ${{i+1}}: ${{p[2]}}</title></circle>`;
    }});

    svg+="</svg>";
    container.innerHTML=svg;
}}

function init() {{
    const nums=allNumbers(DATA);
    document.getElementById("kpis").innerHTML=`
        <div class="kpi"><div class="label">Numeric observations</div><div class="value">${{nums.length}}</div></div>
        <div class="kpi"><div class="label">Data fields</div><div class="value">${{countLeaves(DATA)}}</div></div>
        <div class="kpi"><div class="label">Data source</div><div class="value">Gold</div></div>
    `;

    document.getElementById("status").innerHTML=
        '<span class="badge">Analytics connected</span>'+
        '<span class="badge">Gold data loaded</span>'+
        '<span class="badge">Viewer ready</span>';

    document.getElementById("visualInfo").innerHTML=
        "<p class='small'>The current viewer renders a generic numeric observation graph from the Gold output. The next integration will let the Visualization Intelligence Engine choose the exact visualization and send its graph-ready data here.</p>";

    document.getElementById("raw").textContent=
        JSON.stringify(DATA,null,2);

    buildTable();
    drawChart();
}}

init();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path != "/":
            self.send_response(404)
            self.end_headers()
            return

        body = page().encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8765
    print("==============================================")
    print(" MARKET INTELLIGENCE VISUALIZATION VIEWER")
    print("==============================================")
    print(f"Open on this device : http://127.0.0.1:{port}")
    print(f"LAN access           : http://<PHONE-IP>:{port}")
    print("----------------------------------------------")
    print("Press CTRL+C to stop.")
    print("==============================================")
    HTTPServer((host, port), Handler).serve_forever()
