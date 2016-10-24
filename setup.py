"""
Created on Oct 23, 2016

@author: ahmadjaved.se@gmail.com
"""
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='CloudSearch-Logger',
      version='0.2',

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

      install_requires=['boto==2.42.0', 'requests'],

      extras_require=dict(
          test=['mock==1.0.1', 'testscenarios==0.2', 'testtools==0.9.34']
      ),

      include_package_data=True,

      zip_safe=False)
