terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.49.0"
    }
  }
}

provider "aws" { # configurações específicas
  region = "us_east_1"
}