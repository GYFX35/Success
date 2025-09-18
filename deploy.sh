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
echo "Building and pushing Docker images..."
gcloud builds submit --config cloudbuild.yaml .

# Deploy backend to Cloud Run
echo "Deploying backend to Cloud Run..."
gcloud run deploy backend \
  --image="gcr.io/$GOOGLE_CLOUD_PROJECT/backend:latest" \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080

# Get the backend URL
BACKEND_URL=$(gcloud run services describe backend --platform=managed --region=us-central1 --format='value(status.url)')

# Deploy frontend to Cloud Run
echo "Deploying frontend to Cloud Run..."
gcloud run deploy frontend \
  --image="gcr.io/$GOOGLE_CLOUD_PROJECT/frontend:latest" \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --set-env-vars=BACKEND_URL=$BACKEND_URL

echo "Deployment complete."
echo "Frontend URL: $(gcloud run services describe frontend --platform=managed --region=us-central1 --format='value(status.url)')"
