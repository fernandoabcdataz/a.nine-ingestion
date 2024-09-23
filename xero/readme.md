# Data Fetching Service

This repository contains a Cloud Run service that fetches data from API endpoints (currently Xero) and stores it in Google Cloud Storage using Python's multiprocessing for efficient data processing.

## Overview

The service is designed to run on Google Cloud Platform and uses the following technologies:

- Python 3.9
- Flask
- Google Cloud Run
- Google Cloud Storage
- Google Secret Manager
- Google BigQuery

## Key Features

- Parallel data fetching from multiple API endpoints using multiprocessing
- Implements pagination for handling large datasets
- Rate limiting to comply with API restrictions
- Error handling and retry logic
- Efficient data storage in Google Cloud Storage
- Creates BigQuery tables for easy data analysis

## Structure

- `main.py`: Entry point for the Flask application
- `data_pipeline.py`: Contains the multiprocessing logic for data processing
- `config.py`: Configuration management
- `authentication.py`: Handles authentication with the API
- `api_client.py`: Manages API calls, including pagination and rate limiting
- `data_storage.py`: Handles interactions with Google Cloud Storage
- `table_loader.py`: Sets up BigQuery raw tables
- `utils.py`: Utility functions (e.g., logging)
- `Dockerfile`: Defines the container for the Cloud Run service
- `requirements.txt`: Lists Python dependencies

## Setup

1. Clone this repository
2. Ensure you have the Google Cloud SDK installed and configured
3. Build and push the Docker image:
   ```bash
   docker build -t gcr.io/[PROJECT-ID]/data-fetching-xero:latest .
   docker push gcr.io/[PROJECT-ID]/data-fetching-xero:latest
	 ```

## Deployment

This service is designed to be deployed using Terraform. The Terraform configuration should:

	1.	Create a Google Cloud Storage bucket
	2.	Set up Google Secret Manager secrets for API credentials
	3.	Deploy the Cloud Run service
	4.	Configure a Cloud Scheduler job to trigger the service periodically

Refer to the Terraform configuration in the infrastructure repository for details.

## Usage

Once deployed, the service can be triggered via an HTTP POST request to the /run endpoint. This will initiate the data fetching process, process it using multiprocessing, and store the results in the configured Google Cloud Storage bucket.

## Environment Variables

The service expects the following environment variables:

	•	CLIENT_NAME: The name of the client (used in naming resources)
	•	GOOGLE_CLOUD_PROJECT: The Google Cloud Project ID

These should be set in the Cloud Run service configuration.

## Performance Considerations

	•	The service uses Python’s multiprocessing for parallel processing of multiple API endpoints, significantly improving performance for large datasets.
	•	Pagination is handled within each endpoint’s processing, ensuring all data is fetched efficiently.
	•	Rate limiting is implemented to respect API usage limits while maximizing throughput.

## Security

	•	API credentials are stored in Google Secret Manager
	•	The service uses a dedicated service account with minimal necessary permissions
	•	All communication is done over HTTPS

## Monitoring and Logging

Logs are available in Google Cloud Console under the Cloud Run service. The service uses structured logging for better observability. Consider setting up log-based metrics and alerts for production use.

## Contributing

	1.	Fork the repository
	2.	Create your feature branch (git checkout -b feature/AmazingFeature)
	3.	Commit your changes (git commit -m 'Add some AmazingFeature')
	4.	Push to the branch (git push origin feature/AmazingFeature)
	5.	Open a Pull Request

## License

Distributed under the MIT License. See LICENSE for more information.
