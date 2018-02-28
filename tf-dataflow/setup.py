import setuptools
# from pip.req import parse_requirements
#
# # parse_requirements() returns generator of pip.req.InstallRequirement objects
# install_reqs = parse_requirements('requirements.txt')
#
# requirements = [str(ir.req) for ir in install_reqs]

requirements = ['tensorflow', 'protobuf', 'six==1.10', 'google-cloud-dataflow']
setuptools.setup(
    name='TF-DATAFLOW-DEMO',
    version='v1',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    package_data={'process': ['model/*', 'model/variables/*']},
)