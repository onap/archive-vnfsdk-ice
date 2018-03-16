#!/bin/sh

sed -i "s/DEBUG =.*/DEBUG = ${DEBUG}/g" ${ICE_SETTINGS}
sed -i "s/MSB_ADDR =.*/MSB_ADDR = \"${MSB_ADDR}\"/g" ${ICE_SETTINGS}
sed -i "s/MSB_PORT =.*/MSB_PORT = \"${MSB_PORT}\"/g" ${ICE_SETTINGS}

/usr/local/bin/python app.py