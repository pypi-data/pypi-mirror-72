from os.path import normpath
from setuptools import setup, find_packages
from robot_math import __version__, __author__, __author_email__, __git_url__

with open(normpath('README.md'), 'r') as rm:
    long_description = rm.read()

setup(
    name='robotframework-calculator',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'robotframework>3'
    ],
    url=__git_url__,
    license='MIT',
    author=__author__,
    author_email=__author_email__,
    description='Extension for Robotframework converting data packet, time str and percent into numeric objects',
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    package_data={
        '': [
            'tests/*.robot',
            'tests/*.html'
        ]
    }
)
