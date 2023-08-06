"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='ezreal',
    version='1.0a2',
    description='An application of services.',
    long_description='Ezreal is a service distributor. '
                     'It exploits different tools and framework around the league of legends environment and gathers '
                     'their functionalities in order to serve functions to feed interfaces. '
                     'Its initial design serves the EzrealBot interface, a bot for discord. ',
    long_description_content_type='text/markdown',
    url='https://github.com/maximeheliot/ezreal',
    author='An aspiring data scientist enthousiast',
    author_email='maxime.heliotpro@example.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Customer Service",
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='services, framework, tool, leagueoflegends, statistics',
    packages=["ezreal", "ezreal/core", "ezreal/utils"],
    python_requires='>=3.7, <4',
    install_requires=['cassiopeia',
                      'SQLAlchemy'],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/maximeheliot/ezreal/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/ezreal/',
    },
)