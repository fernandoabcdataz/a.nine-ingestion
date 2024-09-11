import os
from flask import Flask, jsonify, request
from pipeline import run_pipeline
from config import get_client_config
from bigquery_setup import create_external_tables
import structlog
import traceback
from ratelimit import limits, sleep_and_retry

app = Flask(__name__)
logger = structlog.get_logger()

CONFIG = get_client_config()

@sleep_and_retry
@limits(calls=5, period=60)  # Limit to 5 calls per minute
@app.route('/run', methods=['POST'])
def trigger_pipeline():
    try:
        bucket_name = CONFIG['BUCKET_NAME']
        
        run_pipeline(bucket_name)
        create_external_tables()
        return jsonify({"message": "pipeline completed successfully and BigQuery tables created"}), 200
    except Exception as e:
        error_message = f"Pipeline error: {str(e)}"
        logger.error(error_message, traceback=traceback.format_exc())
        return jsonify({"error": error_message}), 500

@app.route('/', methods=['GET'])
def home():
    return "Xero API Service is running", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)