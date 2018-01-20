try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'C inclusion analyzer',
    'author': 'Andrey Dubas',
    'url': 'github',
    'download_url': 'github',
    'author_email': 'andreydubas1991@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['inclusion_analysis'],
    'scripts': [],
    'name': 'inclusion_analysis',
    'test_suite': 'tests',
}

setup(**config)
