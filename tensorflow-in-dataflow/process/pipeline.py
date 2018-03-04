import apache_beam as beam
import inference

dataset_size = 10000

HEADER = ['weight_pounds', 'is_male', 'mother_age', 'mother_race', 'plurality',
          'gestation_weeks', 'mother_married',
          'cigarette_use', 'alcohol_use']

source_query = """
        SELECT
          weight_pounds,
          is_male,
          mother_age,
          mother_race,
          plurality,
          gestation_weeks,
          mother_married,
          cigarette_use,
          alcohol_use
        FROM
          publicdata.samples.natality
        WHERE year > 2000
        AND weight_pounds > 0
        AND mother_age > 0
        AND plurality > 0
        AND gestation_weeks > 0
        AND month > 0
        LIMIT {}
    """.format(dataset_size)


def process_row(bq_row):

    # modify opaque numeric race code into human-readable data
    races = dict(zip([1, 2, 3, 4, 5, 6, 7, 18, 28, 39, 48],
                     ['White', 'Black', 'American Indian', 'Chinese',
                      'Japanese', 'Hawaiian', 'Filipino',
                      'Asian bq_row', 'Korean', 'Samaon', 'Vietnamese']))
    instance = dict()

    instance['is_male'] = str(bq_row['is_male'])
    instance['mother_age'] = bq_row['mother_age']

    if 'mother_race' in bq_row and bq_row['mother_race'] in races:
        instance['mother_race'] = races[bq_row['mother_race']]
    else:
        instance['mother_race'] = 'Unknown'

    instance['plurality'] = bq_row['plurality']
    instance['gestation_weeks'] = bq_row['gestation_weeks']
    instance['mother_married'] = str(bq_row['mother_married'])
    instance['cigarette_use'] = str(bq_row['cigarette_use'])
    instance['alcohol_use'] = str(bq_row['alcohol_use'])
    instance['weight_pounds'] = str(bq_row['weight_pounds'])

    return instance


def estimate(instance, inference_type):

    weight_pounds = instance.pop('weight_pounds')

    if inference_type == 'local':
        estimated_weight = inference.estimate_local(instance)
    else:
        estimated_weight = inference.estimate_clme(instance)

    instance['estimated_weight'] = estimated_weight
    instance['weight_pounds'] = weight_pounds

    return instance


def to_csv(instance):

    csv_row = ','.join([str(instance[k]) for k in HEADER])
    csv_row += ',{}'.format(instance['estimated_weight'])
    return csv_row


def run_pipeline(inference_type, sink_location, runner, args=None):

    options = beam.pipeline.PipelineOptions(flags=[], **args)

    pipeline = beam.Pipeline(runner, options=options)

    (
            pipeline
            | 'Read from BigQuery' >> beam.io.Read(beam.io.BigQuerySource(query=source_query, use_standard_sql=True))
            | 'Process BQ Row' >> beam.Map(process_row)
            | 'Compute Estimate - {}'.format(inference_type) >> beam.Map(lambda instance: estimate(instance, inference_type))
            | 'Convert to CSV' >> beam.Map(to_csv)
            | 'Write to Sink ' >> beam.io.Write(beam.io.WriteToText(sink_location,
                                                                   file_name_suffix='.csv',
                                                                   #num_shards=2
                                                                    ))
    )

    job = pipeline.run()
    if runner == 'DirectRunner':
        job.wait_until_finish()
