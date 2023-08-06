from setuptools import setup
with open('DESCRIPTION.txt') as file:
    long_descriptionx = file.read()
setup(name = "temp-converter",
      version = '1.0',
      description = "Convert temperatures easily here.",
      url = "https://github.com/kailash1011/temp-converter",
      author = "Kailash Sharma",
      author_email = "kailashps.1011@gmail.com",
      license = "MIT",
      long_description = long_descriptionx,
      classifiers = ['Programming Language :: Python :: 3.6'],
      )