"""
Setup to install heluxup as a Python package.
"""

from datetime import datetime
from os import getenv
from setuptools import find_packages, setup


def readme():
    """
    Read the full README.md file as a string.
    """
    with open('README.md') as file_read:
        return file_read.read()


def requirements():
    """
    Read the requirements.txt file as a list of strings.
    """
    with open('requirements.txt') as file_read:
        requirements_file = file_read.readlines()
    return [r.strip() for r in requirements_file]


setup(
    name='heluxup',
    version=getenv('GITHUB_REF', default=datetime.now().strftime('%Y.%m.%d.dev%H%M%S')).lstrip('refs/tags/'),
    description='heluxup makes it easy to upgrade HelmRelease objects in a flux control respository.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ekeih/heluxup',
    author='Max Rosin',
    author_email='heluxup@hackrid.de',
    license='GPL',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.7',
    install_requires=requirements(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'heluxup=heluxup.main:cli'
        ]
    }
)
