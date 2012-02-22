from setuptools import setup, find_packages
import os
import fnmatch

version = '3.1.0'


def find_doctests(top):
    for dirpath, dirnames, filenames in os.walk(top):
        for filename in fnmatch.filter(filenames, '*.dt'):
            yield dirpath + '/' + filename


def read(rname):
    if os.path.isfile(rname):
        return open(os.path.join(os.path.dirname(__file__), rname)).read()
    return ''


long_description = (
    read('README.rst')
    )


setup(name='ludibrio',
      version=version,
      description="Platform for test doubles in Python (mocks, stubs, and dummies)",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mock stub fake dummy doubles mocks',
      author='nsigustavo@gmail.com',
      author_email='Gustavo Rezende',
      url='http://nsigustavo.blogspot.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      setup_requires=['nose'],
      test_suite='nose.collector',
      use_2to3=True,
      convert_2to3_doctests=list(find_doctests('ludibrio/specification')),
      )

