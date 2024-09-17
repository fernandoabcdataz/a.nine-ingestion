import multiprocessing
from config import CONFIG
from api_client import fetch_data_from_endpoint
from data_storage import write_json_to_gcs
from utils import get_logger
import json
from datetime import datetime

logger = get_logger()

DETAILED_ENDPOINTS = [
    'accounts', 'bank_transactions', 'bank_transfers', 'batch_payments', 'budgets',
    'contact_groups', 'contacts', 'credit_notes', 'invoices', 'manual_journals', 'payments'
]

# Mapping of endpoint names to their corresponding ID field names
ID_FIELD_MAPPING = {
    'accounts': 'AccountID',
    'bank_transactions': 'BankTransactionID',
    'bank_transfers': 'BankTransferID',
    'batch_payments': 'BatchPaymentID',
    'budgets': 'BudgetID',
    'contact_groups': 'ContactGroupID',
    'contacts': 'ContactID',
    'credit_notes': 'CreditNoteID',
    'invoices': 'InvoiceID',
    'manual_journals': 'ManualJournalID',
    'payments': 'PaymentID'
}

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
            
            if name in DETAILED_ENDPOINTS:
                logger.info(f"Processing summary data for detailed endpoint: {name}")
                json_lines = "\n".join(json.dumps({**item, "ingestion_time": ingestion_time}) for item in all_data)
                write_json_to_gcs(CONFIG['BUCKET_NAME'], f"{name}_summary.json", json_lines)
                logger.info(f"Processed summary for endpoint {name}, total records: {len(all_data)}")
                
                logger.info(f"Starting ID iteration for detailed endpoint: {name}")
                detailed_data = []
                id_field = ID_FIELD_MAPPING.get(name)
                if id_field:
                    for item in all_data:
                        if id_field in item:
                            detailed_endpoint = f"{endpoint}/{item[id_field]}"
                            logger.debug(f"Fetching detailed data for {name} with ID: {item[id_field]}")
                            detailed_item = fetch_data_from_endpoint(detailed_endpoint)  # No offset for detailed calls
                            if detailed_item:
                                detailed_item['ingestion_time'] = ingestion_time
                                detailed_data.append(detailed_item)
                        else:
                            logger.warning(f"ID field '{id_field}' not found in item for endpoint {name}")
                else:
                    logger.error(f"ID field mapping not found for endpoint {name}")
                
                if detailed_data:
                    logger.info(f"Writing detailed data for endpoint: {name}")
                    detailed_json_lines = "\n".join(json.dumps(item) for item in detailed_data)
                    write_json_to_gcs(CONFIG['BUCKET_NAME'], f"{name}_detailed.json", detailed_json_lines)
                    logger.info(f"Processed detailed data for endpoint {name}, total records: {len(detailed_data)}")
                else:
                    logger.warning(f"No detailed data found for endpoint {name}")
            else:
                logger.info(f"Processing data for non-detailed endpoint: {name}")
                json_lines = "\n".join(json.dumps({**item, "ingestion_time": ingestion_time}) for item in all_data)
                write_json_to_gcs(CONFIG['BUCKET_NAME'], f"{name}.json", json_lines)
                logger.info(f"Processed endpoint {name}, total records: {len(all_data)}")
        else:
            logger.warning(f"No data found for endpoint {name}")
    except Exception as e:
        logger.error(f"Error processing endpoint {name}: {str(e)}", exc_info=True)

def run_pipeline():
    with multiprocessing.Pool() as pool:
        pool.map(process_endpoint, CONFIG['ENDPOINTS'].items())

if __name__ == "__main__":
    run_pipeline()