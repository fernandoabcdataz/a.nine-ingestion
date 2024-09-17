import requests
from authentication import get_token
from utils import get_logger
from requests.exceptions import RequestException, HTTPError
from ratelimit import limits, sleep_and_retry
import time

logger = get_logger()

MAX_RETRIES = 5
BASE_BACKOFF_TIME = 5  # seconds

@sleep_and_retry
@limits(calls=50, period=60)  # reduced to 50 calls per minute to be more conservative
def fetch_data_from_endpoint(endpoint, offset=None):
    token = get_token()
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Accept': 'application/json'}
    params = {'offset': offset} if offset is not None else {}

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Fetching data from {endpoint}" + (f" - Offset {offset}" if offset is not None else ""))
            response = requests.get(endpoint, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if offset is not None:
                # this is a summary endpoint call
                # extract the actual data items from the response
                actual_data = next((value for key, value in data.items() if isinstance(value, list)), [])
                return actual_data
            else:
                # this is a detailed endpoint call
                return data # return the entire response for detailed calls

        except HTTPError as e:
            if e.response.status_code == 429:
                wait_time = BASE_BACKOFF_TIME * (2 ** attempt)
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"HTTP error occurred: {e}")
                raise
        except RequestException as e:
            logger.error(f"Failed to fetch data from {endpoint}" + (f" - Offset {offset}" if offset is not None else f": {str(e)}"))
            raise

    logger.error(f"Max retries reached for {endpoint}. Giving up.")
    raise Exception(f"Failed to fetch data after {MAX_RETRIES} attempts")