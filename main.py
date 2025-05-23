from scrapers.remoteok_scraper import scrape_remoteok
from scrapers.jobrapido_scraper import scrape_jobrapido
from export_excel import export_jobs_to_excel

def main():
    all_jobs = []
    all_jobs += scrape_remoteok()
    all_jobs += scrape_jobrapido()
    export_jobs_to_excel(all_jobs)

if __name__ == "__main__":
    main()