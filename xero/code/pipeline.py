import json
import structlog
from config import CONFIG
from api import fetch_data_from_endpoint
from storage import write_json_to_gcs
from ratelimit import limits, sleep_and_retry

logger = structlog.get_logger()

@sleep_and_retry
@limits(calls=1, period=5)  # Limit to 1 call per 5 seconds
def process_endpoint(name, endpoint, bucket_name):
    try:
        logger.info("processing_endpoint", name=name)
        all_data = []
        page = 1
        while True:
            data, has_more = fetch_data_from_endpoint(endpoint, page)
            if not data:
                logger.info("no_data_received", endpoint=name, page=page)
                break
            all_data.extend(data)
            if not has_more:
                break
            page += 1

        if all_data:
            json_lines = "\n".join(json.dumps(item) for item in all_data)
            write_json_to_gcs(bucket_name, f"{name}.json", json_lines)
            logger.info("endpoint_processed", name=name, total_records=len(all_data))
        else:
            logger.info("no_data_to_process", name=name)
    except Exception as e:
        logger.error("error_processing_endpoint", name=name, error=str(e))
        raise

def run_pipeline(bucket_name):
    for name, endpoint in CONFIG['ENDPOINTS'].items():
        try:
            process_endpoint(name, endpoint, bucket_name)
        except Exception as e:
            logger.error(f"Failed to process endpoint {name}: {str(e)}")
            # Decide whether to continue with other endpoints or stop the pipeline
            # For now, we'll continue with other endpoints
            continue

    logger.info("Pipeline completed")