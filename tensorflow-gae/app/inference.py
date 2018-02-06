import tensorflow as tf

SAVED_MODEL_DIR = 'models/babyweight-estimator-v1'


def estimate(instance):

    instance = dict((k, [v]) for k, v in instance.items())

    predictor_fn = tf.contrib.predictor.from_saved_model(
        export_dir= SAVED_MODEL_DIR,
        signature_def_key="predict"
    )

    value = predictor_fn(instance)['predictions'][0][0]
    output = {"estimate": str(value)}
    return output
