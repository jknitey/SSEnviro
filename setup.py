from setuptools import setup, find_packages

setup(
    author='Josh Knight',
    description='One stop shop for all your environmental data requests.',
    name='SSEnviro',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'meteostat',
        'pandas',
        'requests',
        'json',
        'datetime',
    ], 
    python_requires='>=3.8.8',
    license="MIT",
    keywords=["weather", "data", "timeseries", "meteorology", "soil", "agriculture"],
)