terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  s3_use_path_style           = true  # Correct parameter name for AWS provider
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3  = "http://localhost:4566"
    iam = "http://localhost:4566"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "reddit_bucket" {
  bucket = "rabbitmq-reddit"  # Unique bucket name
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.reddit_bucket.id
  acl    = "private"
}

data "aws_iam_policy_document" "bucket_access" {
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.reddit_bucket.arn,
      "${aws_s3_bucket.reddit_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_user" "reddit_user" {
  name = "reddit-user"
}

resource "aws_iam_user_policy" "reddit_user_policy" {
  name   = "reddit-bucket-access"
  user   = aws_iam_user.reddit_user.name
  policy = data.aws_iam_policy_document.bucket_access.json
}

resource "aws_iam_access_key" "reddit_user_key" {
  user = aws_iam_user.reddit_user.name
}

output "aws_access_key_id" {
  value = aws_iam_access_key.reddit_user_key.id
}

output "aws_secret_access_key" {
  value     = aws_iam_access_key.reddit_user_key.secret
  sensitive = true
}

output "bucket_name" {
  value = aws_s3_bucket.reddit_bucket.bucket
}