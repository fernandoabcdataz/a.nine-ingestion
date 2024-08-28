from flask import Flask, jsonify
from pipeline import run_pipeline
from config import BUCKET_NAME
import os
import structlog
import traceback

app = Flask(__name__)
logger = structlog.get_logger()

@app.route('/run', methods=['POST'])
def trigger_pipeline():
    try:
        run_pipeline(BUCKET_NAME)
        return jsonify({"message": "Pipeline completed successfully"}), 200
    except Exception as e:
        error_message = f"Pipeline error: {str(e)}"
        logger.error(error_message, traceback=traceback.format_exc())
        return jsonify({"error": error_message}), 500

@app.route('/', methods=['GET'])
def home():
    return "Xero API Service is running", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))