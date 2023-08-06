from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='catchphrase',
    version='0.1.0',
    packages=['catchphrase'],
    url='https://github.com/scnerd/catchphrase',
    license='MIT',
    author='David Maxson',
    author_email='scnerd@gmail.com',
    description='Holy Hooligan Coders, Batman! A python package for generating/retrieving common catchphrases!',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
