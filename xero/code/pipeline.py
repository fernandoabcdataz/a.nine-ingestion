import multiprocessing
from config import CONFIG
from api import fetch_data_from_endpoint
from storage import write_json_to_gcs
import json
from datetime import datetime
import structlog

logger = structlog.get_logger()

def process_endpoint(name_endpoint):
    name, endpoint = name_endpoint
    all_data = []
    page = 1
    try:
        while True:
            data, has_more = fetch_data_from_endpoint(endpoint, page)
            if not data:
                break
            all_data.extend(data)
            if not has_more:
                break
            page += 1

        if all_data:
            ingestion_time = datetime.utcnow().isoformat()
            json_lines = "\n".join(json.dumps({**item, "ingestion_time": ingestion_time}) for item in all_data)
            write_json_to_gcs(CONFIG['BUCKET_NAME'], f"{name}.json", json_lines)
        return f"Processed {name}"
    except Exception as e:
        logger.error(f"Error processing {name}: {str(e)}")
        return f"Failed to process {name}: {str(e)}"

def run_pipeline(bucket_name):
    with multiprocessing.Pool() as pool:
        results = pool.map(process_endpoint, CONFIG['ENDPOINTS'].items())
    return [r for r in results if r]  # Filter out None results

if __name__ == "__main__":
    run_pipeline(CONFIG['BUCKET_NAME'])