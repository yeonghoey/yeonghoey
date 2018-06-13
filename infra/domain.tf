locals {
  domain = "yeonghoey.com"
}

data "aws_route53_zone" "main" {
  name = "${local.domain}"
}
