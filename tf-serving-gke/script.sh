GCP_PROJECT=ksalama-gcp-playground
BASE_IMAGE_NAME=tensorflow-serving
IMAGE_NAME=babyweight-serving
GKE_CLUSTER_NAME=ks-cluster-demo
ZONE=europe-west1-b



docker build --pull -t gcr.io/${GCP_PROJECT}/${BASE_IMAGE_NAME} -f tf-serving-base.Dockerfile .

gcloud docker -- push gcr.io/${GCP_PROJECT}/${BASE_IMAGE_NAME}



docker build -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME} -f babyweight-serving.Dockerfile .


gcloud docker -- push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}



gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${ZONE} --project ${GCP_PROJECT}



kubectl apply -f babyweight-serving-pod.yaml


kubectl expose pod babyweight-serving --type=LoadBalancer --name=babyweight-serving-service

