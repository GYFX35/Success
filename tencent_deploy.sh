#!/bin/bash

# This script deploys a static website to Tencent Cloud Object Storage (COS).
# It uses the AWS CLI, which is compatible with Tencent COS S3 API.
#
# Prerequisites:
# 1. AWS CLI installed (pip install awscli)
# 2. AWS CLI configured with Tencent Cloud credentials.
#    - Create a new API key on the Tencent Cloud console: https://console.cloud.tencent.com/cam/capi
#    - Configure the AWS CLI with the SecretId and SecretKey:
#      aws configure
#      AWS Access Key ID [None]: <Your-SecretId>
#      AWS Secret Access Key [None]: <Your-SecretKey>
#      Default region name [None]: <Your-Region>
#      Default output format [None]: json
#
# Usage:
# ./tencent_deploy.sh <bucket-name> <region>
# e.g., ./tencent_deploy.sh my-static-website ap-guangzhou

set -e

BUCKET_NAME=$1
REGION=$2
ENDPOINT_URL="cos.${REGION}.myqcloud.com"

if [ -z "$BUCKET_NAME" ] || [ -z "$REGION" ]; then
  echo "Usage: $0 <bucket-name> <region>"
  exit 1
fi

echo "Creating COS bucket: ${BUCKET_NAME}"
aws --endpoint-url "https://${ENDPOINT_URL}" s3 mb "s3://${BUCKET_NAME}"

echo "Configuring bucket for static website hosting..."
aws --endpoint-url "https://${ENDPOINT_URL}" s3 website "s3://${BUCKET_NAME}" --index-document "index.html" --error-document "index.html"

echo "Uploading website files from docs/ ..."
aws --endpoint-url "https://cos.${REGION}.myqcloud.com" s3 sync docs/ "s3://${BUCKET_NAME}" --acl public-read

WEBSITE_URL="http://${BUCKET_NAME}.cos-website.${REGION}.myqcloud.com"
echo "Deployment complete. Your website is available at:"
echo "${WEBSITE_URL}"
