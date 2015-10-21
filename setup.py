import os
import sys

from setuptools import setup, find_packages, Command

import laser_range_finder

def get_reqs(testing=False):
    return [
        'Pillow>=2.3.0',
        'numpy>=1.8.2',
    ]

setup(
    name='laser_range_finder',
    version=laser_range_finder.__version__,
    description='Calculates distance using images taken with a generic webcam and a low-power laser',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='https://github.com/chrisspen/laser_range_finder',
    license='MIT License',
    packages=find_packages(),
    install_requires=get_reqs(),
    zip_safe=True,
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        #'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['OS Independent'],
    cmdclass={
        #'test': TestCommand,
    },
)
