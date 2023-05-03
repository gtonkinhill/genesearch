import requests
from bs4 import BeautifulSoup
import logging


def call_google_search_api(api_key, engine_id, query):
    # Define the API endpoint
    url = "https://www.googleapis.com/customsearch/v1"

    # Define the query parameters
    params = {"key": api_key, "cx": engine_id, "q": query}

    # Make the GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        search_results = response.json()
        return search_results
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return None


def download_text_from_url(url, min_word_count=100):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            long_paragraphs = []
            for paragraph in paragraphs:
                text = paragraph.get_text()
                word_count = len(text.split())

                if word_count >= min_word_count:
                    long_paragraphs.append(text)

            return long_paragraphs
        else:
            logging.error(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error downloading text from URL: {url}. Error: {e}")
        return None


def download_text_from_search_results(results, num_results=10):
    if results:
        items = results.get("items", [])
        texts = []
        for index, item in enumerate(items[:num_results]):
            url = item.get("link")
            logging.info(f"Downloading text from result {index + 1}: {url}")
            text = download_text_from_url(url)
            if text:
                texts.append(text)

        return texts
    else:
        logging.warning("No results found.")
        return []
