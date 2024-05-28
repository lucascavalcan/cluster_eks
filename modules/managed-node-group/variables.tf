variable "project_name" {
  type        = string
  description = "Project name to be used to name the resources"
}

variable "tags" {
  type        = map(any)
  description = "tags to be add to AWS resources"
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name to create MNG"
}

variable "subnet_private_1a" {
  type        = string
  description = "subnet id from AZ 1a"
}

variable "subnet_private_1b" {
  type        = string
  description = "subnet id from AZ 1b"
}