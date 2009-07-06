from setuptools import setup, find_packages
import sys, os
import re
version = '0.0'



def read(*rnames):
    return file(os.path.join(os.path.dirname(__file__), *rnames)).read()


text = (
    read('ludibrio/__init__.py')
    )
init = text.find('"""')
fim = text.find('"""', init+1)
long_description = text[init:fim]


setup(name='ludibrio',
      version=version,
      description="Platform for test doubles in Python (mocks, stubs, fakes, and dummies)",
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
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
