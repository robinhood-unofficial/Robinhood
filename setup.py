"""Setup.py for Robinhood helper library"""

from os import path, listdir
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = path.abspath(path.dirname(__file__))
__version__ = '1.0.0'

def include_all_subfiles(*args):
    """Slurps up all files in a directory (non recursive) for data_files section

    Note:
        Not recursive, only includes flat files

    Returns:
        (:obj:`list` :obj:`str`) list of all non-directories in a file

    """
    file_list = []
    for path_included in args:
        local_path = path.join(HERE, path_included)

        for file in listdir(local_path):
            file_abspath = path.join(local_path, file)
            if path.isdir(file_abspath):    #do not include sub folders
                continue
            file_list.append(path_included + '/' + file)

    return file_list

class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'Tests',
            '--cov=Robinhood/',
            '--cov-report=term-missing'
        ]    #load defaults here

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest_commands = []
        try:    #read commandline
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:  #use defaults
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

setup(
    name='Robinhood',
    author='Jamone Kelly',
    author_email='prospermarketshow@gmail.com',
    url='https://github.com/lockefox/Robinhood',
    download_url='https://github.com/lockefox/Robinhood/tarball/v' + __version__,
    version=__version__,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='Robinhood trade API',
    packages=find_packages(),
    data_files=[
        ('docs', include_all_subfiles('docs')),
        ('tests', include_all_subfiles('tests'))
    ],
    package_data={

    },
    install_requires=[
        'requests~=2.13.0',
        'six~=1.10.0'
    ],
    tests_require=[
        'pytest~=3.0.0',
        'pytest_cov~=2.4.0'
    ],
    cmdclass={
        'test':PyTest
    }
)
