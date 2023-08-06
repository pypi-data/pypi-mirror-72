#!/usr/bin/env python
from __future__ import absolute_import
import os
try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test

here = os.path.dirname(os.path.abspath(__file__))

setup(
    name='bahram-cli',
    version='1.4.7',
    entry_points={
        'console_scripts': [
            'bahram=f:run',
        ],
    },
    scripts=['f.py'],
    author='bahram',
    author_email='admin@tokyodevs.com',
    url='https://github.com/tokyodevs/deded',
    description='Faster Development For Django 3 Projects',
    packages=find_packages(),
    long_description="long_description  f ew f ew f 4ew f we",
    long_description_content_type='text/markdown',
    keywords='django',
    zip_safe=False,
    install_requires=[
        "PyInquirer",
        "fire",
        "yaspin",
        "requests",
        # "alive-progress",
        #               "appdirs",
        #               "argcomplete",
        #               "certifi",
        #               "chardet",
        #               "click",
        #               "colorama",
        #               "docopt",
        #
        #               "idna",
        #               "importlib-metadata",
        #               "milc",
        #               "prompt-toolkit==1.0.14",
        #               "Pygments",
        #
        #               "regex",
        #
        #               "six",
        #               "termcolor",
        #               "urllib3",
        #               "wcwidth",
        #
        #               "zipp",
    ],
    include_package_data=True,
    # cmdclass={},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
