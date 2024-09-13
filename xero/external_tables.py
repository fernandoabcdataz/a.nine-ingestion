from google.cloud import bigquery
from config import CONFIG
from utils import get_logger

logger = get_logger()

def create_external_tables():
    client = bigquery.Client(project=CONFIG['PROJECT_ID'])
    dataset_id = f"{CONFIG['PROJECT_ID']}.{CONFIG['CLIENT_NAME']}_ingestion"

    for endpoint in CONFIG['ENDPOINTS'].keys():
        table_id = f"{dataset_id}.xero_{endpoint}"
        external_config = bigquery.ExternalConfig("NEWLINE_DELIMITED_JSON")
        external_config.source_uris = [f"gs://{CONFIG['BUCKET_NAME']}/{endpoint}.json"]
        external_config.autodetect = True

        table = bigquery.Table(table_id)
        table.external_data_configuration = external_config

        try:
            client.delete_table(table_id, not_found_ok=True)
            client.create_table(table)
            logger.info(f"Created external table {table_id}")
        except Exception as e:
            logger.error(f"Error creating table for {endpoint}: {str(e)}")

if __name__ == "__main__":
    create_external_tables()