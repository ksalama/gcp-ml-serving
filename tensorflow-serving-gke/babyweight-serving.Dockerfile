FROM gcr.io/ksalama-gcp-playground/tensorflow-serving

COPY babyweight-estimator /babyweight-estimator/
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]