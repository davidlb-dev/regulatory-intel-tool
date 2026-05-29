# Regulatory Intel Tool

> Monitors regulatory publications from SEC, CFTC, FCA, Basel, and the Federal Reserve — and generates structured impact assessments using AI.

---

## What It Does

The Regulatory Intel Tool automatically fetches the latest publications from five major financial regulators and analyzes each one using Claude (Anthropic's AI) to produce structured compliance impact assessments.

For each publication, the tool outputs:
- **Relevance** — High / Medium / Low
- **Risk Level** — High / Medium / Low
- **Affected Parties** — who in the industry is impacted
- **Key Action Required** — what firms need to do
- **Timeline** — immediate / 30 days / 90 days / monitoring only
- **Analyst Note** — 2-3 sentences of context and insight

Results are sorted by risk level and displayed as color-coded cards in a browser interface.

---

## Live Demo

[https://web-production-98d42.up.railway.app](https://web-production-98d42.up.railway.app)

---

## Why It Exists

Compliance and risk teams at financial services firms spend significant time manually monitoring regulatory publications across multiple jurisdictions. This tool automates the monitoring and triage layer — surfacing what matters, assessing impact, and flagging required actions.

Built by [Bond River Partners](https://bondriverpartners.net/).

---

## Architecture

The tool has three layers:

| Layer | File | What It Does |
|-------|------|--------------|
| Fetch | `fetchers.py` | Pulls RSS feeds from SEC, CFTC, FCA, Basel, and Federal Reserve |
| Analyze | `analyzer.py` | Sends each publication to Claude API with a compliance analyst prompt |
| Display | `app.py` | Flask web server that renders results as color-coded cards |

---

## Regulatory Sources

| Source | Feed Type |
|--------|-----------|
| SEC | Press releases and rule proposals |
| CFTC | General press releases |
| FCA | News and press releases |
| Basel (BIS) | BCBS publications |
| Federal Reserve | All press releases |

---

## How To Run It

### Prerequisites
- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Setup

```bash
git clone https://github.com/davidlb-dev/regulatory-intel-tool.git
cd regulatory-intel-tool
python3 -m venv venv
source venv/bin/activate
pip install anthropic flask requests feedparser python-dotenv
```

Create a `.env` file in the project root:

ANTHROPIC_API_KEY=your_key_here

### Run

```bash
python app.py
```

Open `http://localhost:5000` in your browser and click **Run Analysis**.

---

## AI Layer

Regulatory analysis is powered by [Claude](https://anthropic.com) (claude-sonnet-4-5). Each publication is sent to the API with a structured prompt instructing Claude to act as a compliance analyst and return assessments in a consistent format. The prompt is designed to produce actionable, structured output rather than general summaries.

---

## Roadmap

- [x] SEC, CFTC, FCA, Basel, Federal Reserve fetchers
- [x] Claude-powered impact assessments
- [x] Browser UI with color-coded risk cards
- [ ] Filter by source and risk level
- [ ] Email or Slack alerts for High risk items
- [ ] Persistent storage to avoid re-analyzing seen publications
- [ ] Public deployment

---

## Built With

- [Python](https://python.org)
- [Flask](https://flask.palletsprojects.com)
- [Anthropic Claude API](https://anthropic.com)
- [feedparser](https://feedparser.readthedocs.io)

## Author

David Boadita — [Bond River Partners](https://bondriverpartners.net/)