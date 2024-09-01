# Xero Data Pipeline
This project implements a data pipeline to fetch data from the Xero API and store it in Google Cloud Storage. It uses Google Cloud Run for serverless deployment and Cloud Scheduler for automated hourly data retrieval.

## Project Structure

```
ingestion
├── code/
  ├── main.py
  ├── config.py
  ├── auth.py
  ├── api.py
  ├── pipeline.py
  ├── storage.py
  ├── requirements.txt
  └── Dockerfile
├── terraform/
  ├── main.tf
  ├── variables.tf
  └── terraform.tfvars
├── README.md
```

## Prerequisites

- Google Cloud Platform account
- Xero Developer account
- Terraform installed locally
- Google Cloud SDK installed locally

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/your-username/xero-data-pipeline.git
   cd xero-data-pipeline
   ```

2. Create a `terraform.tfvars` file with your specific values:
   ```
   xero_client_id     = "YOUR_XERO_CLIENT_ID"
   xero_client_secret = "YOUR_XERO_CLIENT_SECRET"
   project            = "YOUR_GCP_PROJECT_ID"
   client_name        = "YOUR_CLIENT_NAME"
   region             = "YOUR_PREFERRED_REGION"
   ```

3. Ensure you have a Google Cloud service account key file named `service-account.json` in the parent directory of this project.

## Deployment
1. Initialize Terraform:
   ```
   terraform init
   ```

2. Plan the Terraform changes:
   ```
   terraform plan
   ```

3. Apply the Terraform configuration:
   ```
   terraform apply
   ```

4. Build and push your Docker image to Google Container Registry:
   
   Option 1: Using Google Cloud Build (Recommended)
   ```
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/xero-api
   ```

   Option 2: Local Build and Push
   ```
   docker build -t gcr.io/YOUR_PROJECT_ID/xero-api .
   gcloud auth configure-docker
   docker push gcr.io/YOUR_PROJECT_ID/xero-api
   ```

   Replace `YOUR_PROJECT_ID` with your actual Google Cloud Project ID.

5. The Cloud Run service will automatically use the newly pushed image as specified in the Terraform configuration.

## Usage
Once deployed, the Cloud Scheduler will automatically trigger the Cloud Run service every hour to fetch data from Xero and store it in Google Cloud Storage.

You can also manually trigger the pipeline by sending a POST request to the Cloud Run service URL (output after Terraform apply).

## Configuration

- Modify `config.py` to adjust the Xero API endpoints you want to fetch data from.
- Update `pipeline.py` if you need to change the data processing logic.
- Adjust the Cloud Scheduler cron job in `main.tf` if you want to change the frequency of data fetching.

## Security

- Xero API credentials are stored securely in Google Secret Manager.
- A dedicated service account is used for the Cloud Run service with minimal necessary permissions.
- Ensure that `terraform.tfvars` and `service-account.json` are not committed to version control.

## Monitoring and Maintenance

- Use Google Cloud's operations suite (formerly Stackdriver) to monitor the Cloud Run service and view logs.
- Regularly review and rotate the Xero API credentials and the service account key used for Terraform execution.
- Monitor the usage and costs associated with the deployed resources in the Google Cloud Console.

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.