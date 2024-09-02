import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from config import CONFIG
from api import fetch_data_from_endpoint
from storage import WriteJSONToGCS
import json
import structlog

logger = structlog.get_logger()

class FetchDataFromEndpoints(beam.DoFn):
    def process(self, element):
        for name, endpoint in CONFIG['ENDPOINTS'].items():
            logger.info("processing_endpoint", name=name)
            try:
                data = fetch_data_from_endpoint(endpoint)
                if not data:
                    logger.info("no_data_received", endpoint=name)
                    continue
                json_lines = "\n".join(json.dumps(item) for item in data)
                yield {
                    'endpoint_name': name,
                    'file_content': json_lines
                }
            except Exception as e:
                logger.error("error_processing_endpoint", name=name, error=str(e))

def run_pipeline(bucket_name):
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DirectRunner'

    with beam.Pipeline(options=options) as p:
        results = (
            p
            | 'Start' >> beam.Create([None])
            | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints())
            | 'WriteToGCS' >> beam.ParDo(WriteJSONToGCS(bucket_name))
        )

    logger.info("Pipeline completed")