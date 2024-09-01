variable "xero_client_id" {
  description = "Xero API Client ID"
  type        = string
  sensitive   = true
}

variable "xero_client_secret" {
  description = "Xero API Client Secret"
  type        = string
  sensitive   = true
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "australia-southeast1"
}

variable "client_name" {
  description = "Client Name"
  type        = string
}

variable "service_account_email" {
  description = "email of the service account to use for the Xero API service"
  type        = string
}