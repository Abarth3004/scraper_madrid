import requests
from bs4 import BeautifulSoup
from filters import is_valid_job

def scrape_remoteok():
    url = "https://remoteok.com/remote-marketing-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    rows = soup.select("tr.job")
    print(f"[REMOTEOK] Jobs found: {len(rows)}")
    for row in rows:
        title = row.select_one("td.position h2").get_text(strip=True)
        company = row.select_one("td.company h3").get_text(strip=True)
        url = "https://remoteok.com" + row.get("data-href", "")
        location = row.select_one("div.location")
        summary = title
        if location:
            summary += " - " + location.get_text(strip=True)
        combined = f"{title} {summary}"
        if is_valid_job(combined):
            jobs.append({
                "source": "RemoteOK",
                "title": title,
                "company": company,
                "location": "Remote",
                "summary": summary,
                "url": url
            })
    return jobs