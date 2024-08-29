provider "google" {
  project     = var.project
  region      = var.region
  credentials = file("../service-account.json")
}

resource "google_storage_bucket" "xero_data_bucket" {
  name          = "${var.project}-${var.client_name}-xero-data"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_secret_manager_secret" "client_id" {
  secret_id = "xero-client-id"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "client_id_version" {
  secret      = google_secret_manager_secret.client_id.id
  secret_data = var.xero_client_id
}

resource "google_secret_manager_secret" "client_secret" {
  secret_id = "xero-client-secret"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "client_secret_version" {
  secret      = google_secret_manager_secret.client_secret.id
  secret_data = var.xero_client_secret
}

resource "google_project_iam_member" "xero_api_sa_roles" {
  for_each = toset([
    "roles/secretmanager.secretAccessor",
    "roles/storage.objectCreator"
  ])
  role    = each.key
  member  = "serviceAccount:${var.service_account_email}"
  project = var.project
}

resource "google_cloud_run_service" "xero_api" {
  name     = "${var.project}-${var.client_name}-xero-api"
  location = var.region

  template {
    spec {
      service_account_name = var.service_account_email
      containers {
        image = "gcr.io/${var.project}/xero-api:latest"
        env {
          name  = "CLIENT_NAME"
          value = var.client_name
        }
        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.project
        }
        env {
          name = "CLIENT_ID"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.client_id.secret_id
              key  = "latest"
            }
          }
        }
        env {
          name = "CLIENT_SECRET"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.client_secret.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "allUsers" {
  location = google_cloud_run_service.xero_api.location
  project  = google_cloud_run_service.xero_api.project
  service  = google_cloud_run_service.xero_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# resource "google_cloud_run_service_iam_member" "invoker" {
#   location = google_cloud_run_service.xero_api.location
#   project  = google_cloud_run_service.xero_api.project
#   service  = google_cloud_run_service.xero_api.name
#   role     = "roles/run.invoker"
#   member   = "serviceAccount:${var.service_account_email}"
# }

resource "google_cloud_scheduler_job" "xero_api_scheduler" {
  name        = "${var.project}-${var.client_name}-xero-api-scheduler"
  description = "Scheduler job to invoke Cloud Run service every hour"
  schedule    = "0 * * * *"
  time_zone   = "UTC"

  http_target {
    http_method = "POST"
    uri         = google_cloud_run_service.xero_api.status[0].url

    oidc_token {
      service_account_email = var.service_account_email
      audience              = google_cloud_run_service.xero_api.status[0].url
    }
  }

  attempt_deadline = "320s"

  depends_on = [google_cloud_run_service.xero_api]
}

locals {
  ingestion_dataset_id = "${var.client_name}_ingestion"
  gcs_bucket_name      = "${var.project}-${var.client_name}-xero-data"
}

resource "google_bigquery_dataset" "ingestion_dataset" {
  project    = var.project
  dataset_id = local.ingestion_dataset_id
  location   = var.region

  labels = {
    environment = "dev"
  }

  # Add this to prevent destruction of the dataset if it already exists
  lifecycle {
    prevent_destroy = true
  }
}

data "google_storage_bucket_objects" "xero_files" {
  bucket = local.gcs_bucket_name
}

resource "google_bigquery_table" "external_tables" {
  for_each = { for obj in data.google_storage_bucket_objects.xero_files.items : obj.name => obj if endswith(obj.name, ".json") }

  project    = var.project
  dataset_id = local.ingestion_dataset_id
  table_id   = "xero_${replace(each.key, ".json", "")}"

  external_data_configuration {
    autodetect    = true
    source_format = "NEWLINE_DELIMITED_JSON"
    source_uris   = ["gs://${local.gcs_bucket_name}/${each.key}"]
  }

  depends_on = [google_bigquery_dataset.ingestion_dataset]
}

output "ingestion_dataset_id" {
  value = local.ingestion_dataset_id
}