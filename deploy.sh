#!/bin/bash

# Exit on error
set -e

# Check for gcloud
if ! [ -x "$(command -v gcloud)" ]; then
  echo 'Error: gcloud is not installed.' >&2
  exit 1
fi

# Get project ID
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
  read -p "Enter your Google Cloud project ID: " GOOGLE_CLOUD_PROJECT
fi

if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
  echo "Error: No Google Cloud project ID provided."
  exit 1
fi

# Set the project
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Enable APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Submit the build to Cloud Build
echo "Starting the build and deployment process..."
gcloud builds submit --config cloudbuild.yaml .

echo "Cloud Build has been triggered. Monitor the build progress in the Google Cloud Console."
