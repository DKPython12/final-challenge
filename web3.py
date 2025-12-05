import requests
from bs4 import BeautifulSoup

base_url = "https://web3.career"

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def extract_web3_jobs(keyword, max_pages=30):
    jobs_db = []
    seen_links = set()
    page = 1

    while page <= max_pages:
        url = f"{base_url}/{keyword}-jobs?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find_all("tr", class_="table_row")

        new_this_page = 0

        for job in jobs:
            a = job.find("a", href=True)
            if not a:
                continue

            link = f"{base_url}/{a['href']}"

            if link in seen_links:
                continue

            title_tag = job.find("h2")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            if not title:
                continue

            seen_links.add(link)
            new_this_page += 1

            company_name_tag = job.find("h3")
            company_name = company_name_tag.get_text(strip=True)
            #location_tag = job.find("td", class_="job-location-mobile")
            #location = location_tag.get_text(strip=True)
            salary_tag = job.find("p", class_="ps-0 mb-0 text-salary")
            salary = salary_tag.get_text(strip=True)

            job_data = {
                "title":title,
                "company_name":company_name,
                #"location":location,
                "salary":salary,
                "link": link
            }

            jobs_db.append(job_data)

        if new_this_page == 0:
            break

        page += 1

    return jobs_db



