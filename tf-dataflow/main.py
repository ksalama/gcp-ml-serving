import datetime
import os
import shutil
import logging
from process import pipeline


#RUNNER = 'DirectRunner'
RUNNER = 'DataflowRunner'
PROJECT = 'ksalama-gcp-playground'
BUCKET = 'ksalama-gcs-cloudml'

local_dir = 'local_data'
gcs_dir = 'gs://{0}/data/babyweight/tf-data-out'.format(BUCKET)

output_dir = local_dir if RUNNER == 'DirectRunner' else gcs_dir

sink_location = os.path.join(output_dir, 'data-estimates')

shutil.rmtree(output_dir, ignore_errors=True)

job_name = 'tf-process-babyweight' + '-' + datetime.datetime.now().strftime('%y%m%d-%H%M%S')
print('Launching Beam job {} - {} ... hang on'.format(RUNNER,job_name))

args = {
    'region': 'europe-west1',
    'staging_location': os.path.join(gcs_dir, 'tmp', 'staging'),
    'temp_location': os.path.join(gcs_dir, 'tmp'),
    'job_name': job_name,
    'project': PROJECT,
    'teardown_policy': 'TEARDOWN_ALWAYS',
    'no_save_main_session': True,
    'setup_file': './setup.py'
}


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  pipeline.run_pipeline(sink_location=sink_location,
               runner=RUNNER,
               args=args)
