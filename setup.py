from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='ludibrio',
      version=version,
      description="Platform for test doubles in Python (mocks, stubs, fakes, and dummies)",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mock stub fake dummy dobles mocks',
      author='nsigustavo@gmail.com',
      author_email='Gustavo Rezende',
      url='nsigustavo.blogspot.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
