

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='EcoNameTranslator',  
     version='2.0',
     author="Daniel Davies",
     author_email="dd16785@bristol.ac.uk",
     description="A lightweight but powerful package for full management and translation of ecological names",
     long_description_content_type='text/markdown',
     long_description=long_description,
     url="https://github.com/Daniel-Davies/MedeinaTranslator",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=['taxon-parser'],
 )