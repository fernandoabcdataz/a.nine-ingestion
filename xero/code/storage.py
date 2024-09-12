from google.cloud import storage

def write_json_to_gcs(bucket_name, file_name, content):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content, content_type='application/json')
    return f"saved {file_name} to gs://{bucket_name}/{file_name}"