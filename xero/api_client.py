import requests
from authentication import get_token
from utils import get_logger
from requests.exceptions import RequestException
from ratelimit import limits, sleep_and_retry

logger = get_logger()

@sleep_and_retry
@limits(calls=60, period=60)  # limit to 60 calls per minute
def fetch_data_from_endpoint(endpoint, offset=None):
    token = get_token()
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Accept': 'application/json'}
    params = {'offset': offset} if offset is not None else {}

    try:
        logger.info(f"fetching data from {endpoint}" + (f" - offset {offset}" if offset is not None else ""))
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
            return data  # return the entire response for detailed calls
    except RequestException as e:
        logger.error(f"failed to fetch data from {endpoint}" + (f" - offset {offset}" if offset is not None else f": {str(e)}"))
        raise