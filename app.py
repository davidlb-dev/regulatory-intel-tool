import os
from dotenv import load_dotenv
import anthropic
from flask import Flask, render_template_string, jsonify
from fetchers import fetch_all
from analyzer import analyze_all

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Regulatory Intel Tool</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 20px; background: #f9f9f9; }
        h1 { color: #2c3e50; }
        .controls { margin-bottom: 24px; }
        button { background: #2c3e50; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; }
        button:hover { background: #1a252f; }
        button:disabled { background: #aaa; cursor: not-allowed; }
        #status { margin-top: 10px; font-size: 14px; color: #666; }
        .item { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
        .item-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
        .source { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; }
        .source-SEC { background: #1a5276; }
        .source-CFTC { background: #1e8449; }
        .source-FCA { background: #6c3483; }
        .source-Basel { background: #b7950b; color: #333; }
        .source-Fed { background: #c0392b; }
        .risk { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .risk-High { background: #fadbd8; color: #922b21; }
        .risk-Medium { background: #fdebd0; color: #935116; }
        .risk-Low { background: #d5f5e3; color: #1e8449; }
        .title { font-size: 16px; font-weight: bold; }
        .title a { color: #2c3e50; text-decoration: none; }
        .title a:hover { text-decoration: underline; }
        .meta { font-size: 12px; color: #888; margin: 6px 0; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0; }
        .field { background: #f4f4f4; border-radius: 4px; padding: 8px 12px; font-size: 13px; }
        .field-label { font-weight: bold; color: #555; font-size: 11px; text-transform: uppercase; }
        .analyst-note { background: #eaf4fb; border-left: 3px solid #2980b9; padding: 10px 14px; font-size: 13px; color: #444; margin-top: 10px; border-radius: 0 4px 4px 0; }
    </style>
</head>
<body>
    <h1>Regulatory Intel Tool</h1>
    <div class="controls">
        <button id="analyzeBtn" onclick="runAnalysis()">Run Analysis</button>
        <div id="status"></div>
    </div>
    <div id="results"></div>

    <script>
        async function runAnalysis() {
            const btn = document.getElementById('analyzeBtn');
            const status = document.getElementById('status');
            const results = document.getElementById('results');

            btn.disabled = true;
            btn.textContent = 'Running...';
            status.textContent = 'Fetching latest publications from SEC, CFTC, FCA, Basel, and Federal Reserve... this takes ~2 minutes';
            results.innerHTML = '';

            try {
                const response = await fetch('/analyze');
                const data = await response.json();

                status.textContent = `${data.length} publications analyzed`;
                data.sort((a, b) => {
                    const order = { 'High': 0, 'Medium': 1, 'Low': 2, 'N/A': 3 };
                    return (order[a.risk_level] ?? 3) - (order[b.risk_level] ?? 3);
                });
                results.innerHTML = data.map(item => `
                    <div class="item">
                        <div class="item-header">
                            <span class="source source-${item.source}">${item.source}</span>
                            <span class="risk risk-${item.risk_level}">${item.risk_level} Risk</span>
                            <span class="risk risk-${item.relevance}">${item.relevance} Relevance</span>
                        </div>
                        <div class="title"><a href="${item.link}" target="_blank">${item.title}</a></div>
                        <div class="meta">${item.published}</div>
                        <div class="grid">
                            <div class="field"><div class="field-label">Affected Parties</div>${item.affected_parties}</div>
                            <div class="field"><div class="field-label">Timeline</div>${item.timeline}</div>
                            <div class="field" style="grid-column: span 2"><div class="field-label">Key Action Required</div>${item.key_action}</div>
                        </div>
                        <div class="analyst-note">${item.analyst_note}</div>
                    </div>
                `).join('');
            } catch (err) {
                status.textContent = 'Error running analysis. Check the terminal.';
            }

            btn.disabled = false;
            btn.textContent = 'Run Analysis';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/analyze")
def analyze():
    items = fetch_all()
    assessments = analyze_all(items)
    return jsonify(assessments)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)