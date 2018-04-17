#!/bin/bash

REGION="europe-west1"
BUCKET="your-bucket-name" # change to your bucket name

MODEL_NAME="you_model_name" # change to your estimator name
MODEL_VERSION="your.model.version" # change to your model version

MODEL_LOCAL_LOCATION='process/model/*'
MODEL_GCP_LOCATION=gs://${BUCKET}

# upload saved model to GCS
gsutil -m cp -r ${MODEL_LOCAL_LOCATION} ${MODEL_GCP_LOCATION}

gsutil ls ${MODEL_GCP_LOCATION}

# deploy model to GCP
gcloud ml-engine models create ${MODEL_NAME} --regions=${REGION}

# deploy model version
gcloud ml-engine versions create ${MODEL_VERSION} --model=${MODEL_NAME} --origin=${MODEL_GCP_LOCATION} --runtime-version=1.4


