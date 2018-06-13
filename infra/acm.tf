# Cloudfront requires ACM placed only in us-east-1
provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

resource "aws_acm_certificate" "main" {
  provider                  = "aws.us-east-1"
  domain_name               = "${local.domain}"
  subject_alternative_names = ["*.${local.domain}"]
  validation_method         = "DNS"
}

resource "aws_route53_record" "acm_validation" {
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  name    = "${aws_acm_certificate.main.domain_validation_options.0.resource_record_name}"
  type    = "${aws_acm_certificate.main.domain_validation_options.0.resource_record_type}"
  records = ["${aws_acm_certificate.main.domain_validation_options.0.resource_record_value}"]
  ttl     = 60
}

# FIXME: This feature seems buggy currently
# # Use "${aws_acm_certificate_validation.main.certificate_arn}"
# # instead of "${aws_acm_certificate.main.arn}".
# # This makes resources wait until the certificate is ready
# resource "aws_acm_certificate_validation" "main" {
#   certificate_arn = "${aws_acm_certificate.main.arn}"
#   validation_record_fqdns = ["${aws_route53_record.acm_validation.fqdn}"]
# }
