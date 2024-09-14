import os
from flask import Flask, jsonify
from data_pipeline import run_pipeline
from table_loader import load_json_to_table
from utils import get_logger

app = Flask(__name__)
logger = get_logger()

@app.route('/run', methods=['POST'])
def trigger_pipeline():
    try:
        run_pipeline()
        load_json_to_table()
        return jsonify({"message": "pipeline completed successfully and BigQuery tables created"}), 200
    except Exception as e:
        error_message = f"Pipeline error: {str(e)}"
        logger.error(error_message)
        return jsonify({"error": error_message}), 500

@app.route('/', methods=['GET'])
def home():
    return "Data Fetching Service is running", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)