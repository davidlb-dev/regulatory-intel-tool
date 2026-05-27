import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_item(item):
    prompt = f"""You are a regulatory compliance analyst at a financial services firm.

Analyze this regulatory publication and return a structured impact assessment.

SOURCE: {item['source']}
TITLE: {item['title']}
PUBLISHED: {item['published']}
SUMMARY: {item['summary']}

Return your assessment in exactly this format:

RELEVANCE: [High / Medium / Low]
AFFECTED PARTIES: [who is affected - e.g. broker-dealers, banks, asset managers]
RISK LEVEL: [High / Medium / Low]
KEY ACTION REQUIRED: [one sentence describing what firms need to do]
TIMELINE: [immediate / 30 days / 90 days / monitoring only]
ANALYST NOTE: [2-3 sentences of context and insight]"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    return parse_assessment(response_text, item)

def parse_assessment(text, item):
    assessment = {
        "source": item["source"],
        "title": item["title"],
        "link": item["link"],
        "published": item["published"],
        "relevance": extract_field(text, "RELEVANCE"),
        "affected_parties": extract_field(text, "AFFECTED PARTIES"),
        "risk_level": extract_field(text, "RISK LEVEL"),
        "key_action": extract_field(text, "KEY ACTION REQUIRED"),
        "timeline": extract_field(text, "TIMELINE"),
        "analyst_note": extract_field(text, "ANALYST NOTE"),
    }
    return assessment

""" def extract_field(text, field_name):
    for line in text.split("\n"):
        if line.startswith(field_name + ":"):
            return line[len(field_name) + 1:].strip()
    return "N/A" """

def extract_field(text, field_name):
    for line in text.split("\n"):
        if field_name.lower() in line.lower() and ":" in line:
            return line.split(":", 1)[1].strip()
    return "N/A"
    
def analyze_all(items):
    assessments = []
    for i, item in enumerate(items):
        print(f"Analyzing {i+1}/{len(items)}: {item['title'][:60]}...")
        assessment = analyze_item(item)
        assessments.append(assessment)
    return assessments

if __name__ == "__main__":
    from fetchers import fetch_all
    items = fetch_all()
    print(f"\nAnalyzing {len(items)} items...\n")
    assessments = analyze_all(items)
    for a in assessments:
        print(f"\n[{a['source']}] {a['title']}")
        print(f"Relevance: {a['relevance']} | Risk: {a['risk_level']}")
        print(f"Action: {a['key_action']}")
        print(f"Note: {a['analyst_note']}")