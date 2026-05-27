import os
from dotenv import load_dotenv
import anthropic
from flask import Flask, render_template_string
from fetchers import fetch_all

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Regulatory Intel Tool</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; }
        h1 { color: #2c3e50; }
        .item { border: 1px solid #ddd; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
        .source { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; margin-bottom: 8px; }
        .source-SEC { background: #1a5276; }
        .source-CFTC { background: #1e8449; }
        .source-FCA { background: #6c3483; }
        .source-Basel { background: #b7950b; color: #333; }
        .title { font-size: 16px; font-weight: bold; margin-bottom: 4px; }
        .title a { color: #2c3e50; text-decoration: none; }
        .title a:hover { text-decoration: underline; }
        .meta { font-size: 12px; color: #888; margin-bottom: 8px; }
        .summary { font-size: 14px; color: #555; }
    </style>
</head>
<body>
    <h1>Regulatory Intel Tool</h1>
    <p>{{ item_count }} publications fetched from SEC, CFTC, FCA, and Basel</p>
    {% for item in items %}
    <div class="item">
        <span class="source source-{{ item.source }}">{{ item.source }}</span>
        <div class="title"><a href="{{ item.link }}" target="_blank">{{ item.title }}</a></div>
        <div class="meta">{{ item.published }}</div>
        <div class="summary">{{ item.summary | safe }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    items = fetch_all()
    return render_template_string(HTML_TEMPLATE, items=items, item_count=len(items))

if __name__ == "__main__":
    app.run(debug=True)