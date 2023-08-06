import logging
import os

from git import Repo
from git.exc import GitCommandError

from version import __version__
from dslib.utils.logging import configure_logging, deep_suppress_stdout_stderr
from dslib.wrappers.google.storage import StorageWrapper

# Variables about where to store the file
GSC_PROJECT = 'bbc-business-intelligence-data'
GSC_BUCKET = 'bbc-datascience-libraries'
GSC_DIRECTORY = 'python/'


# Set up logging
configure_logging()
LOGGER = logging.getLogger(__name__)

# Add version
repo = Repo()
try:
    LOGGER.info(f'Create git tag "{__version__}"')
    new_tag = repo.create_tag(__version__, message=f'Automatic tag "{__version__}"')
except GitCommandError as exception:
    raise ValueError(f'Invalid version "{__version__}": change it in dslib/__init__.py') from exception
LOGGER.info('Pushing local changes to remote git repository')
repo.remotes.origin.push(new_tag)

# Create source TAR.GZ package
local_dirpath = f'dist/'
LOGGER.info(f'Building package archive in {local_dirpath}')
with deep_suppress_stdout_stderr():
    os.system(f'python setup.py sdist --dist-dir {local_dirpath}')

# Check versions match
pkg_name = f'dslib-{__version__}.tar.gz'
pkg_local_path = os.path.join(local_dirpath, pkg_name)
assert pkg_name in os.listdir(local_dirpath)
LOGGER.info(f'Package {pkg_local_path} successfully created')

# Load it on Google Cloud Storage and make it public
storage = StorageWrapper.from_params(project=GSC_PROJECT, default_bucket=GSC_BUCKET)
pkg_distant_path = os.path.join(GSC_DIRECTORY, pkg_name)
storage.upload_file(pkg_local_path, pkg_distant_path, replace=False)  # Error if already exists
LOGGER.info(f'Public link to "{__version__}" package: {storage.get_public_url(pkg_distant_path)}')

# Load the "latest" version as well and make it public
pkg_name_latest = f'dslib-latest.tar.gz'
pkg_distant_path_latest = os.path.join(GSC_DIRECTORY, pkg_name_latest)
storage.upload_file(pkg_local_path, pkg_distant_path_latest, replace=True)
LOGGER.info(f'Public link to "latest" package: {storage.get_public_url(pkg_distant_path_latest)}')
