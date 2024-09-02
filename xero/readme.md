# Xero Data Pipeline

This project implements a data pipeline to fetch data from the Xero API and store it in Google Cloud Storage. It uses Google Cloud Run for serverless deployment and Cloud Scheduler for automated hourly data retrieval.

## Project Structure
```
ingestion/
├── code/
│   ├── main.py
│   ├── config.py
│   ├── auth.py
│   ├── api.py
│   ├── pipeline.py
│   ├── storage.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

## Prerequisites

- Google Cloud Platform account
- Xero Developer account
- Google Cloud SDK installed locally
- Python 3.7+ installed locally

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/fernandoabcdataz/a.nine-ingestion
   cd xero-data-pipeline/ingestion
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r code/requirements.txt
   ```

4. Set up environment variables:
   ```
   export XERO_CLIENT_ID="YOUR_XERO_CLIENT_ID"
   export XERO_CLIENT_SECRET="YOUR_XERO_CLIENT_SECRET"
   export GCP_PROJECT_ID="YOUR_GCP_PROJECT_ID"
   export GCP_STORAGE_BUCKET="YOUR_GCS_BUCKET_NAME"
   ```

## Local Development and Testing

1. Run the main script locally:
   ```
   python code/main.py
   ```

2. Run unit tests:
   ```
   python -m unittest discover tests
   ```

## Deployment
1. Build and push your Docker image to Google Container Registry:
   
   ```
   gcloud builds submit --tag gcr.io/${GCP_PROJECT_ID}/xero-api ./code
   ```

2. Deploy to Cloud Run (if not using Terraform):
   ```
   gcloud run deploy xero-api --image gcr.io/${GCP_PROJECT_ID}/xero-api --platform managed
   ```

## Usage

Once deployed, the Cloud Scheduler will automatically trigger the Cloud Run service every hour to fetch data from Xero and store it in Google Cloud Storage.

You can also manually trigger the pipeline by sending a POST request to the Cloud Run service URL.

## Configuration

- Modify `config.py` to adjust the Xero API endpoints you want to fetch data from.
- Update `pipeline.py` if you need to change the data processing logic.

## Monitoring and Logging

1. View Cloud Run logs:
   ```
   gcloud run logs read --service xero-api
   ```

2. Set up Cloud Monitoring alerts:
   - Go to the Google Cloud Console
   - Navigate to Monitoring > Alerting
   - Create alerts for metrics like Cloud Run request count, error rate, etc.

## Data Schema

The data stored in Google Cloud Storage follows this structure:

- `invoices/YYYY-MM-DD/invoices.json`
- `contacts/YYYY-MM-DD/contacts.json`
- `accounts/YYYY-MM-DD/accounts.json`

Each file contains a JSON array of objects as returned by the Xero API.

## Extending the Pipeline

To add a new Xero API endpoint:

1. Add the new endpoint URL to `config.py`
2. Create a new method in `api.py` to fetch data from this endpoint
3. Update `pipeline.py` to process and store the new data type
4. Modify `main.py` to include the new data fetch in the main pipeline

## Troubleshooting

Common issues and solutions:

1. "Permission denied" errors: Ensure the service account has the necessary permissions.
2. Data not appearing in GCS: Check Cloud Run logs for any API or storage errors.
3. Cloud Run container failing to start: Verify the Dockerfile and ensure it's listening on the correct port.

## Security

- Xero API credentials are stored securely in Google Secret Manager.
- A dedicated service account is used for the Cloud Run service with minimal necessary permissions.
- Ensure that any files containing sensitive information are not committed to version control.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.