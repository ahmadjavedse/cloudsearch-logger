"""
Created on Oct 23, 2016

@author: ahmadjaved.se@gmail.com
"""
import pip
from setuptools import setup, find_packages

REQUIREMENTS_FILE_PATH = 'requirements.txt'
TESTS_REQUIREMENTS_FILE_PATH = 'tests-requirements.txt'
LINKS = []  # for repo urls (dependency_links)
REQUIRES = []  # for package names
TESTS_REQUIRES = []  # for package names

requirements = pip.req.parse_requirements(REQUIREMENTS_FILE_PATH,
                                          session=pip.download.PipSession())
tests_requirements = pip.req.parse_requirements(TESTS_REQUIREMENTS_FILE_PATH,
                                                session=pip.download.PipSession())

for item in requirements:
    if getattr(item, 'url', None):  # older pip has url
        LINKS.append(str(item.url))
    if getattr(item, 'link', None):  # newer pip has link
        LINKS.append(str(item.link))
    if item.req:
        REQUIRES.append(str(item.req))  # always the package name

for item in tests_requirements:
    if item.req:
        TESTS_REQUIRES.append(str(item.req))  # always the package name


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='CloudSearch-Logger',
      version='0.1',

      description='Python Logger for Logging Data on Amazon CloudSearch',
      long_description=readme(),

      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2.7',
      ],

      keywords='python cloudsearch logger cloudsearch-logger amazon '
               'cloudsearch logging',

      url='https://github.com/ahmadjavedse/cloudsearch-logger.git',

      author='Ahmad Javed',
      author_email='ahmadjaved.se@gmail.com',

      license='',
      packages=find_packages(exclude=['tests*']),

      install_requires=REQUIRES,
      dependency_links=LINKS,

      extras_require=dict(
          test=TESTS_REQUIRES
      ),

      include_package_data=True,

      zip_safe=False)
