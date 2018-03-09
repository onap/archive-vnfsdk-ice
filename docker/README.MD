Introduction:
=============
This document provides the required steps for :
- generating the docker image of the heat validation rest service
- running the rest server.

Installation steps:
====================
Install following software:
- maven
- docker

Configuration steps:
====================
you can override the defaults settings (declared in default_settings.cfg and prod_settings.cfg)
by setting the env variable with the appropriate values (see Dockerfile for available ENV vars)

How to run?
===========
- make sure that the MSB is running
- build the image : 
- ``$ mvn -P docker clean package``
- run the server in DEBUG mode:
- ``$ docker run --rm --name vnfsdk-ice -d -p 5000:5000 -e DEBUG=True -e MSB_ADDR=<MSB ADDR> -e MSB_PORT=80 onap/vnfsdk/ice``
