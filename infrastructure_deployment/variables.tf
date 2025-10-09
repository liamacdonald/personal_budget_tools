variable "project_id" {
 type        = string
 description = "Project ID where the resources will be deployed"
 sensitive   = true
}

variable "region" {
 type        = string
 description = "Region where resources will be deployed"
 sensitive   = true
}

variable "zone" {
 type        = string
 description = "Zone where resources will be deployed"
 sensitive   = true
}

variable "resource_prefix" {
 type        = string
 description = "Prefix to apply to gcp resources where necessary"
 sensitive   = true
}