from setuptools import setup, find_packages
from os import path
from io import open
import apoastro

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='apoastro',
    version=apoastro.__version__,
    description='two-body and n-body problem',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/clnrp/apoastro',
    author='Cleoner Pietralonga',
    author_email='cleonerp@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy'],

)
