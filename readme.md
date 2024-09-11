# Multi-API Data Ingestion for LLM Applications

## Overview

This repository contains a suite of data ingestion pipelines designed to fetch and store data from various APIs to support Large Language Model (LLM) applications, particularly for text-to-SQL use cases. Our solution provides a flexible and scalable approach to gathering data from multiple sources and storing it in a format optimized for LLM processing.

### Supported APIs

- Xero (Accounting)
- Shopify (E-commerce)
- Google Ads
- Facebook Ads
- Others

## Architecture

Our ingestion pipeline leverages several Google Cloud Platform (GCP) services to ensure scalability, reliability, and ease of management:

- **Cloud Run**: Hosts our serverless application, allowing for on-demand scaling and cost-effective operation.
- **Artifact Registry**: Stores and manages our Docker container images.
- **Cloud Storage**: Acts as an intermediate storage layer for raw API data.
- **BigQuery**: Serves as our data warehouse, providing a powerful query engine for LLM applications.

## Key Features

- Dynamic table creation in BigQuery based on API responses
- Automatic schema detection for flexibility across different API structures
- Efficient data pipeline from API to Cloud Storage to BigQuery
- Support for pagination and rate limiting to handle large datasets and API constraints
- Structured logging for better observability and debugging

## Project Structure

- `/xero`: Xero API integration code
- `/shopify`: Shopify API integration code
- `/google_ads`: Google Ads API integration code
- `/facebook_ads`: Facebook Ads API integration code
- `/other_apis`: Placeholder for other APIs

Each API directory contains:
- `main.py`: Entry point for the Cloud Run service
- `pipeline.py`: Core logic for data fetching and processing
- `config.py`: Configuration management
- `api.py`: API interaction logic
- `storage.py`: Cloud Storage interaction
- `bigquery_setup.py`: BigQuery table creation and management

## Setup and Deployment

This repository focuses on the application code for data ingestion. For infrastructure setup and deployment, please refer to our companion repository: [Link to your Terraform repository]

The Terraform repository handles:
- Cloud Run service deployment
- BigQuery dataset creation
- Cloud Storage bucket setup
- IAM and security configurations

## Usage

To add a new API integration:

1. Create a new directory for the API
2. Implement the required files (main.py, pipeline.py, etc.) following the existing patterns
3. Update the configuration in `config.py` to include the new API endpoints
4. Deploy the new service using the Terraform scripts in the companion repository

## Contributing

We welcome contributions to expand the range of supported APIs or enhance existing integrations. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Implement your changes, adhering to the existing code structure
4. Submit a pull request with a clear description of your improvements

## Contact

For questions or support, please contact [Your Contact Information]