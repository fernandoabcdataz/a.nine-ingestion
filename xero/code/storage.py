from google.cloud import storage
import apache_beam as beam
import structlog

logger = structlog.get_logger()

class WriteJSONToGCS(beam.DoFn):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage_client = None
        self.bucket = None

    def setup(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def process(self, element):
        file_name = f"{element['endpoint_name']}.json"
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(element['file_content'], content_type='application/json')
        logger.info("File saved", file_name=file_name, bucket=self.bucket_name)
        yield f"saved {file_name} to gs://{self.bucket_name}/{file_name}"

    def teardown(self):
        if self.storage_client:
            self.storage_client.close()