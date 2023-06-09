from setuptools import setup, find_packages

setup(
    author='Josh Knight',
    description='One stop shop for all your environmental data requests.',
    name='SSEnviro',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'meteostat>=1.6.5',
        'pandas>=1.5.3',
        'requests>=2.27.1',
    ], 
    python_requires='>=3.8.8',
    license="MIT",
    keywords=["weather", "data", "timeseries", "meteorology", "soil", "agriculture", "agriculture data"],
)