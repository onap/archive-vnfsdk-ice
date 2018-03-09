FROM python:3.6.1

ENV ICE_SETTINGS /opt/ice/ice-server/heat_test/prod_settings.cfg
ENV DEBUG False
ENV MSB_ADDR "127.0.0.1"
ENV MSB_PORT 80

# add application
COPY maven/ /opt/ice
COPY prod_settings.cfg /opt/ice/ice-server/heat_test/
COPY run.sh /opt/ice/ice-server/heat_test/

EXPOSE 5000

# install requirements
# Create the group and user to be used in this container
RUN pip install -r /opt/ice/ice-server/requirements.txt &&\
    pip install -r /opt/ice/validation-scripts/requirements.txt &&\
    pip install dumb-init &&\
    groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask &&\
    chown -R flask:flaskgroup /opt/ice &&\
    chmod +x /opt/ice/ice-server/heat_test/*.sh

USER flask
WORKDIR /opt/ice/ice-server/heat_test
# use dumb-init to translate SIGTERM to SIGINT
# this is needed to gracefully stop flask (and unregister service properly)
ENTRYPOINT ["dumb-init", "--rewrite", "15:2", "--"]
CMD ["./run.sh"]
