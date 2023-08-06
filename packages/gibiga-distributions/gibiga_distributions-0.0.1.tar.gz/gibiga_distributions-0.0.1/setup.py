from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='gibiga_distributions',
      version='0.0.1',
      description='Gaussian distributions',
      author="Greg Izzo",
      author_email="greg.izzo@gmail.com",
      long_description=long_description,
      packages=['gibiga_distributions'],
      zip_safe=False)
