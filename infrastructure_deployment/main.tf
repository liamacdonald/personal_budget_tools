terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}


## Necessary variable
locals {
  version_suffix = formatdate("YYYYMMDDhhmmss", timestamp())
}


# Enable necessary APIs
resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "bigquerydatatransfer.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}


## Create cloud storage bucket for managing all project resources
resource "google_storage_bucket" "project_storage_bucket" {
  name                        = "${var.resource_prefix}_household_budget"
  location                    = var.region
  uniform_bucket_level_access = true
  storage_class = "STANDARD"
  force_destroy               = true
  depends_on = [google_project_service.enabled_apis]
}


resource "google_bigquery_dataset" "raw_financial_dataset" {
  dataset_id  = "raw_financial_data"
  friendly_name = "Raw Financial Data"
  description   = "Raw data from different financial sources"
  location      = var.region
  depends_on = [google_project_service.enabled_apis]
}

resource "google_bigquery_table" "raw_meridian_table" {
  dataset_id = google_bigquery_dataset.raw_financial_dataset.dataset_id
  table_id   = "meridian_raw_transactions"
  
  # Load schema from a JSON file in the same directory
  schema = file("${path.module}/table_schemas/meridian_schema.json")
  depends_on = [google_project_service.enabled_apis,google_bigquery_dataset.raw_financial_data]
}