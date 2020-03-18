from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()
with open("requirements.txt", "r") as fh:
  requires = fh.readlines()
    
setup(
  name='consplit',  
  version='0.1',
  author="Rob Westgeest",
  author_email="rob@qwan.eu",
  description="A utility to split up concepts svg files",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/rwestgeest/consplit",
  packages=find_packages(where='src'),
  package_dir={'':'src'},
  install_requires=requires,
  entry_points = {
    'console_scripts': ['consplit=consplit.command_line:main'],
  },
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
)
