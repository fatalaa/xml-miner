from setuptools import setup
import os

PROPS_FILE_NAME = 'defaultProviders.properties'
PROPS_PATH = os.getcwd() + os.sep + 'xmlminer' + os.sep + 'providers' + os.sep + PROPS_FILE_NAME

setup(
    name='xml-miner',
    version='0.1.0',
    packages=['xmlminer', 'xmlminer.tests', 'xmlminer.mining', 'xmlminer.arial10', 'xmlminer.providers'],
    url='https://github.com/fatalaa/xml-miner.git',
    license='MIT',
    author='Tibor',
    author_email='motibi89@yahoo.com',
    description='',
    install_requires = ['requests == 2.2.1',
                        'xlwt == 0.7.5']
)
