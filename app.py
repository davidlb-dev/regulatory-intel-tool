import os
from dotenv import load_dotenv
import anthropic
from flask import Flask, render_template_string

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Regulatory Intel Tool</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
        h1 { color: #2c3e50; }
        .response { background: #f4f4f4; padding: 20px; border-radius: 8px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Regulatory Intel Tool</h1>
    <h2>API Connection Test</h2>
    <div class="response">{{ response }}</div>
</body>
</html>
"""

@app.route("/")
def index():
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[
            {"role": "user", "content": "In 2-3 sentences, describe what a regulatory intelligence tool for financial services would do."}
        ]
    )
    response_text = message.content[0].text
    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == "__main__":
    app.run(debug=True)