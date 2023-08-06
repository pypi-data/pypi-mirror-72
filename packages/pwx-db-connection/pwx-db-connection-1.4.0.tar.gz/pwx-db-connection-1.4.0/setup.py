from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pwx-db-connection',
    version='1.4.0',
    url='',
    author='Guilherme Rosa Koerich',
    author_email='guilherme@pwx.cloud',
    description='Connection to PostgreSQL and Redis - PWX',
    keywords='connection redis postgres pwx',
    packages=find_packages(exclude=['tests']),
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    install_requires=['redis==3.3.11', 'psycopg2-binary==2.8.4'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>3.4',
)
