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

terraform {
  backend "gcs" {
    bucket = "katie_and_liam_terraform_resources"
  }
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


resource "google_bigquery_dataset" "budget_data" {
  dataset_id  = "budget_data"
  friendly_name = "Reporting Budget Data"
  description   = "Dataset that will house all the data for budgets including the raw import data as well as any additional terraform data"
  location      = var.region
  depends_on = [google_project_service.enabled_apis]
}


#### Raw table definitions
resource "google_bigquery_table" "budget_data" {
  dataset_id = google_bigquery_dataset.budget_data.dataset_id
  table_id   = "meridian_raw_transactions"
  
  # Load schema from a JSON file in the same directory
  schema = file("${path.module}/table_and_view_definitions/meridian_schema.json")
  depends_on = [google_project_service.enabled_apis,google_bigquery_dataset.budget_data]
}


#### Materialized Views
resource "google_bigquery_table" "example_materialized_view" {
  dataset_id = google_bigquery_dataset.budget_data.dataset_id
  table_id   = "consolidated_transaction_list"

  materialized_view {
    query          = file("${path.module}/table_and_view_definitions/consolidates_transaction_list_mv.sql")
    enable_refresh = false
  }
}