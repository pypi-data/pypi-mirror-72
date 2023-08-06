from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='drain3',
    packages=['drain3'],
    version="0.7.4",
    license='MIT',
    description="persistent log parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IBM Research Haifa",
    author_email="david.ohana@ibm.com",
    url="https://github.com/IBM/Drain3",
    download_url='https://github.com/IBM/Drain3/archive/v_01.tar.gz',
    keywords=['drain', 'log', 'parser', 'IBM'],
    install_requires=[
        'jsonpickle==1.4.1',
        'kafka==1.3.5',
        'redis==3.5.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
