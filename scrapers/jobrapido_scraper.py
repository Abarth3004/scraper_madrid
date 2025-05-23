import requests
from bs4 import BeautifulSoup
from filters import is_valid_job

def scrape_jobrapido():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, 4):
        url = f"https://es.jobrapido.com/?w=marketing&l=Madrid&p={page}"
        resp = requests.get(url, headers=headers)
        print(f"[JOBRAPIDO] Page {page} - Status {resp.status_code}")
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("article.job-item")
        print(f"[JOBRAPIDO] Page {page} - Cards: {len(cards)}")
        for card in cards:
            title_tag = card.select_one("h2.job-title")
            company = card.select_one("span.company")
            location = card.select_one("span.location")
            summary = card.get_text(" ", strip=True)
            url_tag = card.select_one("a")
            if not title_tag or not url_tag:
                continue
            title = title_tag.get_text(strip=True)
            job_url = "https://es.jobrapido.com" + url_tag.get("href")
            combined = f"{title} {summary}"
            if is_valid_job(combined):
                jobs.append({
                    "source": "Jobrapido",
                    "title": title,
                    "company": company.get_text(strip=True) if company else "",
                    "location": location.get_text(strip=True) if location else "Madrid",
                    "summary": summary,
                    "url": job_url
                })
    return jobs