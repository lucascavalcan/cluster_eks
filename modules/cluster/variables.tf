variable "project_name" {
  type        = string
  description = "Project name to be used to name the resources"
}

variable "tags" {
  type = map
  description = "tags to be add to AWS resources"
}

variable "public_subnet_1a" {
  type = string
  description = "subnet to create EKS cluster - AZ 1a"
}

variable "public_subnet_1b" {
  type = string
  description = "subnet to create EKS cluster - AZ 1b"
}