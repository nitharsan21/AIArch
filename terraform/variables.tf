variable "billing_account" {
  type        = string
}

variable "org_id" {
  type        = string
}
variable "region" {
  type        = string
  default     = "europe-west3"
}

variable "zone" {
  type        = string
  default     = "europe-west3"
}

variable "prefix" {
  type        = string
  default     = "iarchitect"
}

variable "network_name" {
  type        = string
  default     = "iarchitect-network"
}

variable "subnet_ip" {
  type        = string
  default     = "10.10.10.0/24"
}
variable "subnet_name" {
  type        = string
  default     = "iarchitect-subnet"
}

variable "instance_name" {
  type        = string
  default     = "iarchitect"
}

variable "target_size" {
  type        = number
  default     = 1
}

variable "machine_type" {
  type        = string
  default     = "n1-standard-1"
}

variable "source_image_family" {
  type        = string
  default     = "ubuntu-minimal-1804-lts"
}

variable "source_image_project" {
  type        = string
  default     = "ubuntu-os-cloud"
}

variable "source_image" {
  type        = string
  default     = ""
}

variable "cooldown_period" {
  default     = 60
}

variable "database_version" {
    type = string
    default = "MYSQL_5_7"
}

variable "database_tier" {
    type = string
    default = "db-f1-micro"
}

variable "database_name" {
    type = string
    default = "iarchitect"
}

# Random id for naming
resource "random_id" "id" {
  byte_length = 4
  prefix      = var.prefix
}

locals {
  gcp_service_account_name = "${var.prefix}-iarchitect-app"
  cloud_sql_instance_name = "${random_id.id.hex}-db"
}