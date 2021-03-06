from distutils.core import setup

setup(name='globalte',
      version='0.0.1',
      description='A python package to read and plot global elastic thickness.',
      author='Pascal',
      author_email='pascal.audet@uottawa.ca',
      url='https://github.com/paudetseis/GlobalTe/',
      install_requires = ['numpy', 'matplotlib', 'cartopy'],
      python_requires = '>=3.5',
      packages=['globalte'],
      package_data={'globalte': ['data/*.*']},
      include_package_data=True
      )
