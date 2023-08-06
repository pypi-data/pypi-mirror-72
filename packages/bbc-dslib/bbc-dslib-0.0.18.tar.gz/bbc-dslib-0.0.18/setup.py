import codecs
import os
import re

import setuptools

CURRENT_FILEPATH = os.path.abspath(os.path.dirname(__file__))
VERSION_FILENAME = 'version.py'


def find_version():
    # Source: https://packaging.python.org/guides/single-sourcing-package-version/
    with codecs.open(os.path.join(CURRENT_FILEPATH, VERSION_FILENAME), 'r') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="bbc-dslib",
    version=find_version(),
    author="Raphael Berly",
    author_email="raphael.berly@blablacar.com",
    description="A lib for the Data Science team at Blablacar",
    license='MIT',
    url="https://bitbucket.corp.blablacar.com/projects/lib/repos/dslib",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['humanfriendly', 'pyyaml', 'jinja2', 'GitPython'],
    extras_require={
        'google': ['google-cloud-bigquery>=1.18.0', 'oauth2client', 'grpcio', 'pandas', 'pandas-gbq', 'tqdm',
                   'google-cloud-storage', 'google-api-python-client', 'pyarrow', 'google-cloud-bigquery-storage',
                   'gspread==3.6.0', 'gspread-dataframe==3.0.6'],
        'prophet': ['fbprophet'],
        'database': ['sqlalchemy', 'psycopg2-binary', 'PyMySQL', 'pandas'],
        'testing': ['pytest', 'pytest-cov', 'coverage', 'mock', 'testfixtures'],
    }
)
