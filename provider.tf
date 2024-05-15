terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.49.0"
    }
  }

  backend "s3" {
    bucket = "curso-terraform-lucas"
    key    = "dev/terraform.state"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}