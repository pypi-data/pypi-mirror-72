from setuptools import setup, find_packages
with open('Readme.txt') as file:
    long_descriptionx = file.read()
setup(name = "temppack",
      packages = find_packages(),
      download_url = "https://github.com/kailash1011/temppack/archive/v_0.1.tar.gz",
      version = '1.0',
      description = "Complete module to convert units of temperature.",
      url = "https://github.com/kailash1011/temppack",
      author = "Kailash Sharma",
      author_email = "kailashps.1011@gmail.com",
      license = "MIT",
      classifiers = ['Programming Language :: Python :: 3.6'],
      long_description = long_descriptionx

      )