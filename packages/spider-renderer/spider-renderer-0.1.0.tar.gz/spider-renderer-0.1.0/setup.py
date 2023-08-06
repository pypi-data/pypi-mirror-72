'''Building a modular crawler template system based on Jinja2'''

# Note: To upload this project, you must:

'''
python setup.py sdist
pip install dist/
python setup.py bdist_wheel
pip install twine
twine upload dist/*
'''

import os.path

from setuptools import setup

# What packages are required for this module to be executed?
requires = [
    'requests',
    'jinja2',
]

# Import the README and use it as the long-description.
cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spider-renderer',
    packages=['renderer'],
    version='0.1.0',
    license='Apache 2.0',
    author='White Turing',
    author_email='fu.jiawei@outlook.com',
    description='Building a modular crawler template system based on Jinja2.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ffujiawei/spider-renderer',
    keywords=['spider', 'renderer', 'scrapy'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6.0',
    install_requires=requires,
)
