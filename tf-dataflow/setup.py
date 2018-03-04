import setuptools

requirements = []
setuptools.setup(
    name='TF-DATAFLOW-DEMO',
    version='v1',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    package_data={'process': ['model/*', 'model/variables/*']},
)