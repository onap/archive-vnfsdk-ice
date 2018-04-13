Introduction:
=============
This document provides the required steps for running the 
heat validation rest service in a development environment.
If you only want to run it, go to distribution directory.

Installation steps:
====================
Install following software:
- python 3.4 or latest

Configuration steps:
====================
you can override the defaults settings (declared in default_settings.py)
if needed by pointing the env variable ICE_SETTINGS to a file
with the appropriate values :

``$ export ICE_SETTINGS='/path/to/my/production/settings.py'``

How to run?
===========
 - In command console, cd to directory where this service is installed 
 - use virtualenv if needed
 - ``$ pip install -r requirements.txt``
 - check that everything is ok by running unit tests : ``$ tox``
 - ``$ cd heat_test``
 - ``$ python app.py``
 - Once service is started, check the following url: http://127.0.0.1:5000/onapapi/ice/v1/ui
   you should see a "pong" response in the browser.

Debug/development Mode
==========
 debug mode is activated by default
 in debug mode, the swagger ui is available on http://127.0.0.1:5000/onapapi/ice/v1/ui
