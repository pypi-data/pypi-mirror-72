from setuptools import setup, find_packages
from os import path
from io import open

INSTALL_REQUIRES = []
TEST_REQUIRES = []


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(this_directory, 'namantest', '__version__.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__description__'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=about['__author__'],
      author_email=about['__author_email__'],
      url=about['__url__'],
      download_url=about['__download_url__'],
      license=about['__license__'],
      packages=find_packages(),
      classifiers=[
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries :: Python Modules'
],
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES
)
