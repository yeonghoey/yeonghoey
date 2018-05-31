locals {
  bucket = "yeonghoey-media"
}

resource "aws_s3_bucket" "main" {
  bucket = "${local.bucket}"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    # For pdf.js, SEE: https://github.com/mozilla/pdf.js/issues/3150#issuecomment-71365390
    expose_headers = ["Accept-Ranges", "Content-Range", "Content-Encoding", "Content-Length"]
    max_age_seconds = 3000
  }

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    noncurrent_version_expiration {
      days = 7
    }
  }

  policy = <<EOF
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Effect":"Allow",
      "Principal": {"AWS": "${aws_cloudfront_origin_access_identity.main.iam_arn}"},
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::${local.bucket}"]
    },
    {
      "Effect":"Allow",
      "Principal": {"AWS": "${aws_cloudfront_origin_access_identity.main.iam_arn}"},
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::${local.bucket}/*"]
    }
  ]
}
EOF
}

resource "aws_cloudfront_distribution" "main" {
  origin {
    domain_name = "${aws_s3_bucket.main.bucket_domain_name}"
    origin_id   = "${local.bucket}"

    s3_origin_config {
      origin_access_identity = "${aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path}"
    }
  }

  default_cache_behavior {
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "${local.bucket}"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  default_root_object = "index.html"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = "${aws_acm_certificate.main.arn}"
    ssl_support_method  = "sni-only"
  }

  enabled         = true
  is_ipv6_enabled = true
  comment         = "${local.bucket}"
  aliases         = ["media.${local.domain}"]
  price_class     = "PriceClass_200"
}

resource "aws_cloudfront_origin_access_identity" "main" {
  comment = "${local.bucket}"
}

resource "aws_route53_record" "main" {
  name    = "media.${local.domain}"
  zone_id = "${data.aws_route53_zone.main.zone_id}"
  type    = "A"

  alias {
    name                   = "${aws_cloudfront_distribution.main.domain_name}"
    zone_id                = "${aws_cloudfront_distribution.main.hosted_zone_id}"
    evaluate_target_health = true
  }
}
