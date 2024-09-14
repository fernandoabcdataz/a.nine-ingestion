from google.cloud import bigquery
from google.cloud import storage
from config import CONFIG
from utils import get_logger
import io
import json
import datetime

logger = get_logger()

def load_json_to_table():
    client = bigquery.Client(project=CONFIG['PROJECT_ID'])
    storage_client = storage.Client()
    dataset_id = f"{CONFIG['PROJECT_ID']}.{CONFIG['CLIENT_NAME']}_ingestion"

    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logger.info(f"Dataset {dataset_id} already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'US'  # Adjust location as needed
        client.create_dataset(dataset)
        logger.info(f"Created dataset {dataset_id}")

    for endpoint in CONFIG['ENDPOINTS'].keys():
        table_id = f"{dataset_id}.xero_{endpoint}"

        # Define table schema
        schema = [
            bigquery.SchemaField("ingestion_time", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("data", "JSON", mode="REQUIRED"),
        ]

        table_ref = bigquery.Table(table_id, schema=schema)

        # Create or replace table
        try:
            client.delete_table(table_id, not_found_ok=True)
            client.create_table(table_ref)
            logger.info(f"Created table {table_id}")
        except Exception as e:
            logger.error(f"Error creating table {table_id}: {str(e)}")
            continue

        # Read JSON file from GCS
        try:
            bucket = storage_client.bucket(CONFIG['BUCKET_NAME'])
            blob = bucket.blob(f"{endpoint}.json")
            json_content = blob.download_as_string().decode('utf-8')
        except Exception as e:
            logger.error(f"Error reading JSON file for {endpoint}: {str(e)}")
            continue

        # Prepare data for BigQuery
        buffer = io.StringIO()
        current_time = datetime.datetime.utcnow().isoformat()

        for line in json_content.strip().split('\n'):
            if line.strip():
                try:
                    data_json = json.loads(line)
                    record = {
                        "ingestion_time": current_time,
                        "data": data_json
                    }
                    buffer.write(json.dumps(record) + '\n')
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error for {endpoint}: {str(e)}")
                    continue

        buffer.seek(0)

        # Load data into BigQuery
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        try:
            load_job = client.load_table_from_file(
                buffer,
                table_id,
                job_config=job_config
            )
            load_job.result()  # Wait for the job to complete
            logger.info(f"Loaded data into {table_id}")
        except Exception as e:
            logger.error(f"Error loading data into {table_id}: {str(e)}")

if __name__ == "__main__":
    load_json_to_table()