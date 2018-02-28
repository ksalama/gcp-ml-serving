import tensorflow as tf
import os
import logging

tf.logging.set_verbosity(tf.logging.ERROR)

SAVED_MODEL_DIR = 'model'


def estimate(instance):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    instance = dict((k, [v]) for k, v in instance.items())

    export_dir = os.path.join(dir_path,SAVED_MODEL_DIR)

    predictor_fn = tf.contrib.predictor.from_saved_model(
        export_dir=export_dir,
        signature_def_key="predict"
    )

    value = predictor_fn(instance)['predictions'][0][0]
    return value
