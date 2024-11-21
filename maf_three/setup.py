from setuptools import setup, find_packages
import os

# Function to read the version from maf_three/__init__.py
def get_version():
    version_file = os.path.join('maf_three', '__init__.py')
    with open(version_file, 'r') as f:
        exec(f.read(), globals())
    return __version__

# Read the requirements from requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

# Read the long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='maf_three',
    version=get_version(),
    description='Matter and Form - THREE - Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matter and Form',
    author_email='info@matterandform.net',
    url='https://github.com/Matter-and-Form/three-python-library',
    packages=find_packages(exclude=['tests', 'scripts', 'examples']),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'examples=maf_three.examples:main_cli',
        ],
    },
)