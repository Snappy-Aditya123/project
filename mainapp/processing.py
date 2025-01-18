import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import json


class APIS:
    def __init__(self):
        self.KEYS = json.load(open(r"C:\Users\adity\Desktop\luck\project\mainapp\API.json"))
        # Job API details
        self.JOB_BASE_URL = "https://www.reed.co.uk/api/1.0"
        self.JOB_API_KEY = self.KEYS["API_reed"]

        # News API details
        self.NEWS_BASE_URL = "https://api.thenewsapi.com/v1/news"
        self.NEWS_API_KEY = self.KEYS["News_API"]

        # ONS API details
        self.ONS_BASE_URL = "https://api.beta.ons.gov.uk/v1"

    def search_jobs(self, keywords, location=None, distance=10, min_salary=None, max_salary=None, page=1):
        """
        Search for jobs on Reed API.
        :param keywords: Job keywords (e.g., "Software Engineer").
        :param location: Job location (e.g., "London").
        :param distance: Distance from location in miles (default is 10).
        :param min_salary: Minimum salary filter.
        :param max_salary: Maximum salary filter.
        :param page: Page number for pagination (default is 1).
        :return: List of jobs with IDs and basic details.
        """
        endpoint = f"{self.JOB_BASE_URL}/search"
        params = {
            "keywords": keywords,
            "locationName": location,
            "distanceFromLocation": distance,
            "minimumSalary": min_salary,
            "maximumSalary": max_salary,
            "resultsToTake": 100,
            "resultsToSkip": (page - 1) * 100
        }
        try:
            response = requests.get(endpoint, params=params, auth=HTTPBasicAuth(self.JOB_API_KEY, ""))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs: {e}")
            return None

    def get_job_details(self, job_id):
        """
        Get full job details for a specific job ID.
        :param job_id: The ID of the job.
        :return: A dictionary with detailed job information, including description.
        """
        endpoint = f"{self.JOB_BASE_URL}/jobs/{job_id}"
        try:
            response = requests.get(endpoint, auth=HTTPBasicAuth(self.JOB_API_KEY, ""))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job details: {e}")
            return None

    def get_job_related_news(self, keywords, limit=10):
        """
        Fetch articles from the News API and extract full content from the linked URLs.
        
        :param keywords: Keywords related to the job (e.g., "Software Engineer").
        :param limit: Number of articles to retrieve (default is 10).
        :return: List of dictionaries with titles, links, and full content.
        """
        endpoint = f"{self.NEWS_BASE_URL}/all"
        params = {
            "api_token": self.NEWS_API_KEY,
            "search": keywords,
            "language": "en",
            "limit": limit
        }
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            articles = response.json().get("data", [])

            enriched_articles = []
            for article in articles:
                article_url = article.get("url")
                if article_url:
                    full_content = self._extract_article_content(article_url)
                    enriched_articles.append({
                        "title": article.get("title"),
                        "url": article_url,
                        "content": full_content
                    })
            return enriched_articles
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job-related news: {e}")
            return []
        

    def get_ons_datasets(self, limit=20, offset=0):
        """
        Fetch a list of datasets from the ONS API.

        :param limit: Maximum number of datasets to return (default is 20).
        :param offset: Starting index of the datasets to retrieve.
        :return: A list of datasets.
        """
        endpoint = f"{self.ONS_BASE_URL}/datasets"
        params = {
            "limit": limit,
            "offset": offset
        }
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ONS datasets: {e}")
            return None

    def filter_ons_dataset(self, dataset_id, edition, version, dimensions):
        """
        Filter a dataset from the ONS API based on specific dimensions.

        :param dataset_id: The ID of the dataset.
        :param edition: The edition of the dataset.
        :param version: The version of the dataset.
        :param dimensions: A list of dimensions to filter by (e.g., [{"name": "geography", "options": ["K02000001"]}]).
        :return: Filtered dataset or None on failure.
        """
        endpoint = f"{self.ONS_BASE_URL}/filters?submitted=true"
        payload = {
            "dataset": {
                "id": dataset_id,
                "edition": edition,
                "version": version
            },
            "dimensions": dimensions
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error filtering ONS dataset: {e}")
            return None
    def _extract_article_content(self, url):
        """
        Extract full article content from a URL using web scraping.

        :param url: The URL of the article to scrape.
        :return: Extracted text content of the article or a fallback message if extraction fails.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example: Extract paragraphs
            paragraphs = soup.find_all('p')
            full_content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            return full_content or "Content could not be extracted."
        except requests.exceptions.RequestException as e:
            print(f"Error fetching article content from {url}: {e}")
            return "Failed to retrieve content."
    import requests

class RSSFetcher:
    def __init__(self):
        # Example RSS feed URLs
        self.RSS_FEEDS = [
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",  # Technology news
            "https://www.theguardian.com/uk/technology/rss",  # Technology from The Guardian
            "https://feeds.bbci.co.uk/news/technology/rss.xml"  # Technology from BBC
        ]

    def fetch_rss_articles(self, feed_url):
        """
        Fetch and parse articles from an RSS feed.
        
        :param feed_url: The URL of the RSS feed.
        :return: A list of dictionaries containing article details (title, link, description).
        """
        try:
            response = requests.get(feed_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            articles = []
            for item in soup.find_all("item"):
                title = item.title.text if item.title else "No Title"
                link = item.link.text if item.link else "No Link"
                description = item.description.text if item.description else "No Description"
                pub_date = item.pubDate.text if item.pubDate else "No Publication Date"

                articles.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "pub_date": pub_date
                })
            return articles
        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return []

# Example usage
if __name__ == "__main__":
    fetcher = RSSFetcher()

    for feed_url in fetcher.RSS_FEEDS:
        print(f"Fetching articles from: {feed_url}")
        articles = fetcher.fetch_rss_articles(feed_url)

        if articles:
            print("Articles retrieved:")
            for article in articles[:5]:  # Limit to 5 articles per feed for display
                print(f"- Title: {article['title']}")
                print(f"  Link: {article['link']}")
                print(f"  Description: {article['description'][:200]}...")
                print(f"  Published: {article['pub_date']}")
                print()

# Example usage


# # Example usage
# if __name__ == "__main__":
#     api = APIS()

#     # Example: Search for jobs
#     jobs = api.search_jobs(keywords="Software Engineer", location="London", distance=10, page=1)
#     if jobs:
#         print("Jobs found:", jobs)

#     # Example: Get job details
#     job_id = "12345"  # Replace with a valid job ID
#     job_details = api.get_job_details(job_id)
#     if job_details:
#         print("Job details:", job_details)

#     # Example: Get news related to a job
#     news_articles = api.get_job_related_news(keywords="Software Engineer", limit=10)
#     if news_articles:
#         print("News articles related to the job:")
#         for article in news_articles:
#             print(f"- {article['title']}: {article['url']}")

#     # Example: Get datasets from ONS API
#     datasets = api.get_ons_datasets(limit=5)
#     if datasets:
#         print("ONS Datasets:")
#         for dataset in datasets:
#             print(f"- {dataset['title']} (ID: {dataset['id']})")

#     # Example: Filter a dataset from ONS API
#     filtered_data = api.filter_ons_dataset(
#         dataset_id="cpih01",
#         edition="time-series",
#         version=6,
#         dimensions=[{"name": "geography", "options": ["K02000001"]}]
#     )
#     if filtered_data:
#         print("Filtered ONS Dataset:", filtered_data)



# if __name__ == "__main__":
#     api = APIS()

#     # Fetch news articles related to "Software Engineer"
#     news_articles = api.get_job_related_news(keywords="Software Engineer", limit=3)
#     if news_articles:
#         print("News articles with full content:")
#         for article in news_articles:
#             print(f"Title: {article['title']}")
#             print(f"URL: {article['url']}")
#             print(f"Content: {article['content'][:500]}...")  # Print a snippet of the content
