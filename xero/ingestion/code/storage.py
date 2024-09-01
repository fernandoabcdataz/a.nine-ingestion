from google.cloud import storage
import apache_beam as beam
import structlog
import traceback

logger = structlog.get_logger()

class WriteJSONToGCS(beam.DoFn):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage_client = None
        self.bucket = None

    def setup(self):
        try:
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(self.bucket_name)
            logger.info("Storage client and bucket initialized", bucket_name=self.bucket_name)
        except Exception as e:
            logger.error("Failed to initialize storage client", error=str(e), traceback=traceback.format_exc())
            raise

    def process(self, element):
        try:
            file_name = f"{element['endpoint_name']}.json"
            blob = self.bucket.blob(file_name)
            blob.upload_from_string(element['file_content'], content_type='application/json')
            logger.info("File saved", file_name=file_name, bucket=self.bucket_name)
            yield f"saved {file_name} to gs://{self.bucket_name}/{file_name}"
        except Exception as e:
            logger.error("Failed to save file", file_name=file_name, error=str(e), traceback=traceback.format_exc())
            raise

    def teardown(self):
        if self.storage_client:
            self.storage_client.close()