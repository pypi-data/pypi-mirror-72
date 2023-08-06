from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name = 'var_distributions',
      version = '0.2',
      description = 'Gaussian and Binomial Discription',
      packages = ['var_distributions'],
      author="Apaar Bawa",
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe = False)