import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from config import CONFIG
from api import fetch_data_from_endpoint
from storage import WriteJSONToGCS
import json
import structlog
from datetime import datetime

logger = structlog.get_logger()

class FetchDataFromEndpoints(beam.DoFn):
    def process(self, element):
        name, endpoint = element
        logger.info("processing_endpoint", name=name)
        all_data = []
        page = 1
        while True:
            try:
                data, has_more = fetch_data_from_endpoint(endpoint, page)
                if not data:
                    break
                all_data.extend(data)
                if not has_more:
                    break
                page += 1
            except Exception as e:
                logger.error("error_processing_endpoint", name=name, error=str(e))
                break

        if all_data:
            ingestion_time = datetime.utcnow().isoformat()
            json_lines = "\n".join(json.dumps({**item, "ingestion_time": ingestion_time}) for item in all_data)
            yield {
                'endpoint_name': name,
                'file_content': json_lines
            }
        else:
            logger.info("no_data_to_process", name=name)

def run_pipeline(bucket_name):
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DirectRunner'

    with beam.Pipeline(options=options) as p:
        results = (
            p
            | 'Create Endpoints' >> beam.Create(CONFIG['ENDPOINTS'].items())
            | 'FetchDataFromEndpoints' >> beam.ParDo(FetchDataFromEndpoints())
            | 'WriteToGCS' >> beam.ParDo(WriteJSONToGCS(bucket_name))
        )

    logger.info("Pipeline completed")