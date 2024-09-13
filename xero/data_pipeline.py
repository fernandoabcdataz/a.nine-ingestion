import multiprocessing
from config import CONFIG
from api_client import fetch_data_from_endpoint
from data_storage import write_json_to_gcs
from utils import get_logger
import json
from datetime import datetime

logger = get_logger()

def process_endpoint(name_endpoint):
    name, endpoint = name_endpoint
    all_data = []
    offset = 0
    try:
        while True:
            data = fetch_data_from_endpoint(endpoint, offset)
            if not data:
                break
            all_data.extend(data)
            if len(data) < 100:
                break  # Last batch
            offset += 100  # increment offset by 100
        if all_data:
            ingestion_time = datetime.utcnow().isoformat()
            json_lines = "\n".join(json.dumps({**item, "ingestion_time": ingestion_time}) for item in all_data)
            write_json_to_gcs(CONFIG['BUCKET_NAME'], f"{name}.json", json_lines)
            logger.info(f"Processed endpoint {name}, total records: {len(all_data)}")
        else:
            logger.warning(f"No data found for endpoint {name}")
    except Exception as e:
        logger.error(f"Error processing endpoint {name}: {str(e)}")

def run_pipeline():
    with multiprocessing.Pool() as pool:
        pool.map(process_endpoint, CONFIG['ENDPOINTS'].items())