import requests
import time
from auth import get_token
import structlog

logger = structlog.get_logger()

def fetch_data_from_endpoint(endpoint):
    token = get_token()
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Accept': 'application/json'}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info("fetching_data", endpoint=endpoint, attempt=attempt)
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            for value in data.values():
                if isinstance(value, list):
                    return value
                elif isinstance(value, dict):
                    return [value]
            return []
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                logger.error("failed_to_fetch_data", endpoint=endpoint, attempts=max_retries, error=str(e))
                raise
            time.sleep(2 ** attempt)  # Exponential backoff