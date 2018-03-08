import tensorflow as tf

SAVED_MODEL_DIR = 'models/babyweight-estimator-v1'


predictor_fn = None


def init_predictor():

    global predictor_fn

    if predictor_fn is None:

        predictor_fn = tf.contrib.predictor.from_saved_model(
            export_dir=SAVED_MODEL_DIR,
            signature_def_key="predict"
        )

    return predictor_fn


def estimate(instance):

    instance = dict((k, [v]) for k, v in instance.items())

    predictor_fn = init_predictor()

    value = predictor_fn(instance)['predictions'][0][0]
    output = {"estimate": str(value)}
    return output
