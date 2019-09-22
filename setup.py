from datetime import datetime
from os import getenv
from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as f:
        requirements_file = f.readlines()
    return [r.strip() for r in requirements_file]


setup(
    name='heluxup',
    version=getenv('GITHUB_REF', default=datetime.now().strftime('%Y.%m.%d.dev%H%M%S')),
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
