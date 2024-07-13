from setuptools import setup, find_packages

setup(
    name='web_scraping_utils',
    version='1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)