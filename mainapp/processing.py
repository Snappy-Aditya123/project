import requests
from requests.auth import HTTPBasicAuth

# Constants
BASE_URL = "https://www.reed.co.uk/api/1.0"
API_KEY = "your_api_key_here"  # Replace with your API key

# Search for jobs
def search_jobs(keywords, location=None, distance=10, min_salary=None, max_salary=None, page=1):
    endpoint = f"{BASE_URL}/search"
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
        response = requests.get(endpoint, params=params, auth=HTTPBasicAuth(API_KEY, ""))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return None

# Get job details
def get_job_details(job_id):
    endpoint = f"{BASE_URL}/jobs/{job_id}"
    try:
        response = requests.get(endpoint, auth=HTTPBasicAuth(API_KEY, ""))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job details: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Search for jobs
    jobs = search_jobs(keywords="software engineer", location="London", min_salary=30000, max_salary=70000)
    if jobs:
        print(f"Found {len(jobs.get('results', []))} jobs.")
        for job in jobs.get("results", []):
            print(f"{job['jobTitle']} at {job['employerName']} - {job['locationName']}")
    
    # Get details of a specific job
    job_id = "12345"  # Replace with an actual job ID
    job_details = get_job_details(job_id)
    if job_details:
        print(f"Details for job ID {job_id}: {job_details}")
