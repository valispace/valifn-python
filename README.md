# ValiFN Python Image &middot; [![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic&label=code%20style)](https://github.com/psf/black) [![code quality: pylint](https://img.shields.io/badge/code%20quality-pylint-yellowgreen?style=plastic&label=code%20quality)](https://github.com/PyCQA/pylint) [![code security: bandit](https://img.shields.io/badge/code%20security-bandit-yellow.svg?style=plastic&label=code%20security)](https://github.com/PyCQA/bandit) [![continuous integration](https://github.com/valispace/valifn-python/actions/workflows/continuous_integration.yml/badge.svg?style=plastic&label=continuous%20integration&branch=develop)](https://github.com/valispace/valifn-python/actions/workflows/continuous_integration.yml)

ValiFN provides a way to connect and run scripts from [Valispace](https://github.com/valispace) in a safe and isolated environment.

This repository contains code to generate a `python` image to be used by ValiFN.
You can add and remove requirements at your will and then build the image and replace the original image provided by [Valispace](https://github.com/valispace) using the following instructions:

## How to install a new image

1. Clone the repository
```
$ git clone https://github.com/valispace/valifn-python.git
```

2. Add/remove packages to `requirements.txt`
```
# Valispace packages
valispace>=0.1.16   # Valispace API

# Basic scientifical packages
pint>=0.18          # Python library used for scientific
scipy>=1.7.3        # Python library to define, operate and manipulate physical quantities

# Add other packages here
my_new_package==0.0.1
```

3. Build docker image with tag `valispace/valifn-python:latest`
```
$ docker build . --tag valispace/valifn-python:latest
```

NOTE: If you build the image on your deployment server, you can ignore steps 4, 5 and 6.

4. Save image to a file
```
$ docker save valispace/valifn-python:latest | gzip > valifn-python.tar.gz
```

5. Copy `valifn-python.tar.gz` to your destination

6. Load image to docker
```
$ docker load --input valifn-python.tar.gz
```

7. That's it! You have now replaced ValiFN Python Image to match your needs on your deployment. No restart is needed.


## Documentation

See the [Wiki](https://github.com/valispace/valifn-python/wiki) for details on project setup and usage, as also technical details.


## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/valispace/valifn-python/releases).


## Copyright

Copyright &copy; 2015-present, [Valispace GmbH](https://www.valispace.com/about-us/)
