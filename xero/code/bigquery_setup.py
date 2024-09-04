from google.cloud import bigquery
from config import CONFIG, ENDPOINTS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_external_tables():
    client = bigquery.Client(project=CONFIG['PROJECT_ID'])
    dataset_id = f"{CONFIG['PROJECT_ID']}.{CONFIG['CLIENT_NAME']}_ingestion"

    for endpoint, url in ENDPOINTS.items():
        table_id = f"{dataset_id}.xero_{endpoint}"
        
        schema = [
            bigquery.SchemaField("data", "STRING", mode="NULLABLE"),
        ]

        external_config = bigquery.ExternalConfig("NEWLINE_DELIMITED_JSON")
        external_config.source_uris = [
            f"gs://{CONFIG['BUCKET_NAME']}/{endpoint}.json"
        ]
        external_config.schema = schema

        table = bigquery.Table(table_id, schema=schema)
        table.external_data_configuration = external_config

        try:
            client.create_table(table, exists_ok=True)
            logger.info(f"Created or updated external table {table_id}")
        except Exception as e:
            logger.error(f"Error creating external table {table_id}: {str(e)}")

if __name__ == "__main__":
    create_external_tables()