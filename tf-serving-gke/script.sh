#!/usr/bin/env bash

GCP_PROJECT=ksalama-gcp-playground
BASE_IMAGE_NAME=tensorflow-serving
IMAGE_NAME=babyweight-serving
GKE_CLUSTER_NAME=ks-cluster-demo
ZONE=europe-west1-b

# build tensorflow serving base image
docker build --pull -t gcr.io/${GCP_PROJECT}/${BASE_IMAGE_NAME} -f tf-serving-base.Dockerfile .
# push image to google cloud registry
gcloud docker -- push gcr.io/${GCP_PROJECT}/${BASE_IMAGE_NAME}

# build babyweight serving image
docker build -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME} -f babyweight-serving.Dockerfile .
# push image to google cloud registry
gcloud docker -- push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}

# build k8 cluster on GKE
gcloud container clusters create ${GKE_CLUSTER_NAME} --zone ${ZONE} --machine-type n1-standard-2 --enable-autoscaling --min-nodes 3 --max-nodes 10
# get cluster credentials
gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${ZONE} --project ${GCP_PROJECT}

# deploy pod
kubectl apply -f babyweight-serving-pod.yaml
# expose pod
kubectl expose pod babyweight-serving --type=LoadBalancer --name=babyweight-serving-service

