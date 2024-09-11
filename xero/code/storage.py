from google.cloud import storage
import structlog

logger = structlog.get_logger()

def write_json_to_gcs(bucket_name, file_name, content):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(content, content_type='application/json')
        logger.info("File saved", file_name=file_name, bucket=bucket_name)
    except Exception as e:
        logger.error("Failed to save file", file_name=file_name, error=str(e))
        raise