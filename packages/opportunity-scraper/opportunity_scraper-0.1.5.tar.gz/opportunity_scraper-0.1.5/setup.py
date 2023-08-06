#!/usr/bin/env python3

"""Setup script"""

from setuptools import setup, find_packages

setup(
    name="opportunity_scraper",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests-oauthlib',
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'opportunity_scraper=opportunity_scraper:run',
        ]
    }
)
