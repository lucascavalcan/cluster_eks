variable "cidr_block" {
  type        = string
  description = "Network cidr block to be used for the VPC"
}

variable "project_name" {
  type        = string
  description = "Project name to be used to name the resources"
}

variable "region" {
  type        = string
  description = "AWS region to create the resources"
}

variable "tags" {
  type        = map(any)
  description = "A map of tags to add to all of AWS resources"
}