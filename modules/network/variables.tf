variable "cidr_block" {
  type        = string
  description = "Network cidr block to be used for the VPC"
}

variable "project_name" {
  type        = string
  description = "Project name to be used to name the resources"
}

variable "tags" {
  type = map
  description = "tags to be add to AWS resources"
}