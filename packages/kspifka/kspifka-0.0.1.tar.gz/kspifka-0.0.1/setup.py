from setuptools import setup, find_packages

setup(
    name="kspifka",
    packages=['kspifka'],
    version='0.0.1',
    description="Distributed scraping framework for Python.",
    author="kong",
    author_email='tomngp@163.com',
    url="https://github.com/kwx1996/kspifka",
    classifiers=[],
    install_requires=[
        'twisted',
        'redis',
        'confluent_kafka'
    ]
)
