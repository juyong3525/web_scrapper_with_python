import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)

    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"].strip()
    company, location = html.find(
        "h3", {"class": "mb4"}).find_all("span", recursive=False)
    if company != None:
        company = company.get_text(strip=True)
    else:
        company = None
    if location != None:
        location = location.get_text(strip=True)
    else:
        location = None
    job_id = html["data-jobid"]

    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")

        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        cards = soup.find_all("div", {"class": "-job"})
        for card in cards:
            job = extract_job(card)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
