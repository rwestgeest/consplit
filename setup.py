from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
  name='consplit',  
  version='0.1',
  author="Rob Westgeest",
  author_email="rob@qwan.eu",
  description="A utility to split up concepts svg files",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/rwestgeest/consplit",
  packages=['consplit'],
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
)
