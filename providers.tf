terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "<region>"
  secret_key = "<aws_secret_token>"
  access_key = "<aws_access_key>"
  
}