import requests
import time
from auth import get_token
import structlog
from requests.exceptions import RequestException
from ratelimit import limits, sleep_and_retry

logger = structlog.get_logger()

@sleep_and_retry
@limits(calls=60, period=60)  # limit to 60 calls per minute
def fetch_data_from_endpoint(endpoint, page=1):
    token = get_token()
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Accept': 'application/json'}
    params = {'page': page}
    
    try:
        logger.info("fetching_data", endpoint=endpoint, page=page)
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract the actual data items from the response
        actual_data = []
        for key, value in data.items():
            if isinstance(value, list):
                actual_data = value
                break
        
        # Check for more pages
        has_more = 'Links' in response.headers and any(
            link['rel'] == 'next' for link in requests.utils.parse_header_links(response.headers['Links'])
        )
        
        return actual_data, has_more
    except RequestException as e:
        logger.error("failed_to_fetch_data", endpoint=endpoint, page=page, error=str(e))
        raise