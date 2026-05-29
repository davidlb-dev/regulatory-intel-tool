import requests
import feedparser
from datetime import datetime

def fetch_sec():
    print("Fetching SEC...")
    url = "https://www.sec.gov/news/pressreleases.rss"
    headers = {"User-Agent": "regulatory-intel-tool david@bondriver.com"}
    feed = feedparser.parse(url, request_headers=headers)
    results = []
    for entry in feed.entries[:5]:
        results.append({
            "source": "SEC",
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")[:500]
        })
    print(f"SEC: found {len(results)} items")
    return results

def fetch_cftc():
    print("Fetching CFTC...")
    url = "https://www.cftc.gov/RSS/RSSGP/rssgp.xml"
    headers = {"User-Agent": "regulatory-intel-tool david@bondriver.com"}
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:5]:
        results.append({
            "source": "CFTC",
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")[:500]
        })
    print(f"CFTC: found {len(results)} items")
    return results

def fetch_fca():
    print("Fetching FCA...")
    url = "https://www.fca.org.uk/news/rss.xml"
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:5]:
        results.append({
            "source": "FCA",
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")[:500]
        })
    print(f"FCA: found {len(results)} items")
    return results

def fetch_basel():
    print("Fetching Basel...")
   #url = "https://www.bis.org/rss/bcbs_press.xml"
    url = "https://www.bis.org/doclist/bcbspubls.rss"
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:5]:
        results.append({
            "source": "Basel",
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")[:500]
        })
    print(f"Basel: found {len(results)} items")
    return results

def fetch_fed():
    print("Fetching Federal Reserve...")
    url = "https://www.federalreserve.gov/feeds/press_all.xml"
    headers = {"User-Agent": "regulatory-intel-tool david@bondriver.com"}
    feed = feedparser.parse(url, request_headers=headers)
    results = []
    for entry in feed.entries[:5]:
        results.append({
            "source": "Fed",
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")[:500]
        })
    print(f"Fed: found {len(results)} items")
    return results

def fetch_all():
    all_results = []
    all_results.extend(fetch_sec())
    all_results.extend(fetch_cftc())
    all_results.extend(fetch_fca())
    all_results.extend(fetch_basel())
    all_results.extend(fetch_fed())
    print(f"\nTotal items fetched: {len(all_results)}")
    return all_results

if __name__ == "__main__":
    results = fetch_all()
    for item in results:
        print(f"\n[{item['source']}] {item['title']}")
        print(f"Published: {item['published']}")
        print(f"Link: {item['link']}")