# ValiFn Python Image

ValiFn provides a way to connect and run scripts from Valispace in a safe and isolated environment.

This repository contains code to generate a `python image` to be used by ValiFn.
You can add and remove requirements at your will, build the image and replace the original image provided by Valispace using the following instructions.

## How to install new image

1. Clone repository
```
$ git clone https://github.com/valispace/valifn-python.git
```

2. Add/remove packages `requirements.txt`
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
$ docker build . -t valispace/valifn-python:latest
```

NOTE: If you build image on your deployment server, you can ignore steps 4, 5 and 6.

4. Save image to a file
```
$ docker save valispace/valifn-python:latest | gzip > valifn-python.tar.gz
```

5. Copy `valifn-python.tar.gz` to your destination

6. Load image to docker
```
$ docker load -i valifn-python.tar.gz
```

7. Thats it! You have now replaced ValiFn Python Image to match your needs on your deployment. No restart is needed.
