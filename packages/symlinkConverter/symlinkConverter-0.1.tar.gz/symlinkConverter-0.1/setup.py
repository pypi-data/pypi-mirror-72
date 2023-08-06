from setuptools import setup

setup(name='symlinkConverter',
      version='0.1',
      description='Converts Symlinks to Text files and vice-versa',
      url='https://github.com/oparkins/symlinkConverter',
      author='Owen T. Parkins',
      author_email='oparkins@nibious.com',
			scripts=['./bin/symlinkConverter'],
      packages=['symlinkConverter'],
      zip_safe=False)