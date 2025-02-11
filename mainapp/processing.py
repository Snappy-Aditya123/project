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
            "resultsToTake": 20,
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

    import requests

    def get_news_api_article(self, endpoint="latest-news", query_params=None):
        """
        Fetches articles from the Currents News API.

    Args:
        api_key (str): Your API key for the Currents News API.
        endpoint (str): API endpoint to use ("latest-news" or "search").
        query_params (dict, optional): Query parameters for the API request (e.g., filters).

    Returns:
        dict: A JSON response containing news articles or an error message.
    """
        base_url = "https://api.currentsapi.services/v1/"
        url = f"{base_url}{endpoint}"

    # Set up headers and default query parameters
        headers = {
            "Authorization": "pb5_wizU2aBbFT6zJvxNemWBBkHXyDfd3XJnsAxZJnnqlYYB"
    }



        try:
        # Make the API request
            response = requests.get(url, headers=headers, params=query_params)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    
        # Parse the JSON response
            data = response.json()
            if data.get('status') == 'ok':
                articles = data.get('news', [])
                descriptions = [article['description'] for article in articles if 'description' in article]
                return descriptions
            else:
                return {"error": "Invalid API response or no articles available."}

        except requests.exceptions.RequestException as e:
            return {"error": "Failed to fetch data from the API", "details": str(e)}

        

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
    def get_guardian_articles_with_content(self, keyword):
        api_key = self.KEYS['Guardian_API']  # Replace with your API key
        base_url = "https://content.guardianapis.com/search"
        params = {
        "q": keyword,
        "page-size": 3,
        "order-by": "newest",
        "api-key": api_key,
        "show-fields": "webTitle,webUrl,webPublicationDate,body"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise error for bad status
            data = response.json()

            if data["response"]["status"] == "ok" and data["response"]["total"] > 0:
                articles = data["response"]["results"]
                for i, article in enumerate(articles, 1):
                    print(f"Article {i}:")
                    print(f"Title: {article['webTitle']}")
                    print(f"Published: {article['webPublicationDate']}")
                    print(f"URL: {article['webUrl']}")
                    print(f"Content: {article['fields'].get('body', 'No content available')}...")  # Print first 500 chars
                    print("\n")
                return data
            else:
                print("No relevant articles found.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


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



# # Example usage
# if __name__ == "__main__":
#     API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

#     # Fetch the latest news
#     latest_news = get_news_api_article(API_KEY, endpoint="latest-news", query_params={"language": "en"})
#     print(latest_news)

#     # Fetch historical news based on a search keyword
#     historical_news = get_news_api_article(
#         API_KEY,
#         endpoint="search",
#         query_params={"keywords": "Amazon", "language": "en", "category": "technology"}
#     )
#     print(historical_news)
