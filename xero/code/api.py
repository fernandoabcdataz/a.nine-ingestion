import requests
import time
from auth import get_token
import structlog
from requests.exceptions import RequestException
from ratelimit import limits, sleep_and_retry

logger = structlog.get_logger()

@sleep_and_retry
@limits(calls=5, period=60)  # Limit to 5 calls per minute
def fetch_data_from_endpoint(endpoint, page=1):
    token = get_token()
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Accept': 'application/json'}
    params = {'page': page}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info("fetching_data", endpoint=endpoint, page=page, attempt=attempt)
            response = requests.get(endpoint, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check for pagination information
            has_more = False
            if 'Links' in response.headers:
                links = requests.utils.parse_header_links(response.headers['Links'])
                has_more = any(link['rel'] == 'next' for link in links)
            
            # Extract the actual data from the response
            extracted_data = []
            for key, value in data.items():
                if isinstance(value, list):
                    extracted_data = value
                    break
                elif isinstance(value, dict):
                    extracted_data = [value]
                    break
            
            return extracted_data, has_more
        except RequestException as e:
            if attempt == max_retries - 1:
                logger.error("failed_to_fetch_data", endpoint=endpoint, page=page, attempts=max_retries, error=str(e))
                raise
            time.sleep(2 ** attempt)  # exponential backoff
    
    return [], False  # return empty list and false if all retries failed