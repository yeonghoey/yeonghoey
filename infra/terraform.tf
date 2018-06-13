terraform {
  backend "s3" {
    bucket = "yeonghoey"
    key    = "yeonghoey/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}
