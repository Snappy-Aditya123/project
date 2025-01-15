import requests
from bs4 import BeautifulSoup
import random
import time
import concurrent.futures

url = 'https://uk.indeed.com/jobs?q=software+engineer&start=1&vjk=f8b0ddbf8cf96864'

# Function to make requests to the API
def fetch_content(payload):
    try:
        r = requests.get('https://api.scraperapi.com/', params=payload)
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'html.parser')
        else:
            print(f"Failed to retrieve content. Status code: {r.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

# Extract job links from the main page
def extract_job_links(soup):
    links = []
    if soup:
        divs = soup.find_all('div', class_='job_seen_beacon')
        for item in divs:
            link = item.find('a', href=True)
            if link:
                full_link = f"https://uk.indeed.com{link['href']}"
                links.append(full_link)
    return links

# Extract detailed job information
def extract_job_details(job_url):
    payload = {
        'api_key': '0cf23b94df3ab834e2440af257cdf7ee',
        'url': job_url,
        'device_type': 'desktop',
        'max_cost': '100',
        'session_number': '123'
    }
    soup = fetch_content(payload)
    if not soup:
        return None

    title = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
    company = soup.find('div', class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')
    location = soup.find('div', class_='jobsearch-JobInfoHeader-subtitle')
    salary = soup.find('span', class_='jobsearch-JobMetadataHeader-item')
    description = soup.find('div', class_='jobsearch-jobDescriptionText')

    benefits = []
    responsibilities = []
    qualifications = []

    if description:
        for ul in description.find_all('ul'):
            parent_p = ul.find_previous_sibling('p')
            if parent_p and 'Benefits' in parent_p.text:
                benefits.extend([li.text.strip() for li in ul.find_all('li')])
            elif parent_p and 'Responsibilities' in parent_p.text:
                responsibilities.extend([li.text.strip() for li in ul.find_all('li')])
            elif parent_p and 'Qualifications' in parent_p.text:
                qualifications.extend([li.text.strip() for li in ul.find_all('li')])

    job_type = None
    pay = None
    work_location = None

    if description:
        for p in description.find_all('p'):
            if 'Job Type' in p.text:
                job_type = p.text.split(':')[-1].strip()
            elif 'Pay' in p.text:
                pay = p.text.split(':')[-1].strip()
            elif 'Work Location' in p.text:
                work_location = p.text.split(':')[-1].strip()

    job = {
        'title': title.text.strip() if title else None,
        'company': company.text.strip() if company else None,
        'location': location.text.strip() if location else None,
        'salary': salary.text.strip() if salary else None,
        'benefits': benefits,
        'responsibilities': responsibilities,
        'qualifications': qualifications,
        'job_type': job_type,
        'pay': pay,
        'work_location': work_location
    }
    return job

# Main function to orchestrate scraping
def main():
    payload = {
        'api_key': '0cf23b94df3ab834e2440af257cdf7ee',
        'url': url,
        'device_type': 'desktop',
        'max_cost': '100',
        'session_number': '123'
    }

    soup = fetch_content(payload)
    if not soup:
        print("Failed to extract main page content.")
        return

    job_links = extract_job_links(soup)
    print(f"Found {len(job_links)} job links.")

    joblist = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(extract_job_details, job_url) for job_url in job_links]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                joblist.append(result)

    for job in joblist:
        print(job)

if __name__ == "__main__":
    main()
