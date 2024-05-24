variable "project_name" {
  type        = string
  description = "Project name to be used to name the resources"
}

variable "tags" {
  type        = map(any)
  description = "tags to be add to AWS resources"
}

variable "oidc" {
  type = string
  description = "HTTP URL from OIDC provider of the EKS cluster"
}

variable "cluster_name" {
  type = string
  description = "EKS cluster name" 
}