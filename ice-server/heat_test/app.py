#!flask/bin/python
import atexit
import logging

import connexion
import requests
from connexion.resolver import RestyResolver

config = ''

def create_app():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = connexion.App(__name__, specification_dir='swagger/')

    # load default config
    app.app.config.from_pyfile("default_settings.cfg")
    app.app.config.from_envvar('ICE_SETTINGS', silent=True)
    app.add_api('ice_api.yaml', swagger_ui=app.app.config['DEBUG'], resolver=RestyResolver('ice_validator'))

    return app


def create_test_app():
    print("create_test_app")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('ice_api.yaml', swagger_ui=app.app.config['DEBUG'], resolver=RestyResolver('ice_validator'))
    app.app.testing = True
    return app


def start_app(app):
    logging.info("######################################")
    logging.info("starting server")
    logging.info("######################################")
    global config
    config = app.app.config
    msb_register()
    atexit.register(msb_unregister)
    app.run(port=app.app.config['ICE_PORT'], debug=app.app.config['DEBUG'])


def msb_register():
    try:
        msb_url = config['MSB_URL']
        ice_json = {
            "serviceName": config['ICE_SERVICE_NAME'],
            "version": config['ICE_VERSION'],
            "url": "/onapapi/ice/v1",
            "protocol": "REST",
            "visualRange": "1",
            "nodes": [
                {
                    "ip": config['ICE_ADDR'],
                    "port": config['ICE_PORT'],
                    "ttl": 0
                }
            ]
        }
        resp = requests.post(msb_url, json=ice_json)
        if resp.status_code == 201:
            global registered
            registered = True
            logging.info("registration to '%s' done", msb_url)
        else:
            logging.info("registration to '%s' failed; status_code = '%s'", msb_url, resp.status_code)
    except:
        logging.info("registration to '%s' failed", msb_url)


def msb_unregister():
    try:
        msb_url = "%s/%s/version/%s" % (config['MSB_URL'], config['ICE_SERVICE_NAME'], config['ICE_VERSION'])
        resp = requests.delete(msb_url)
        if resp.status_code == 200:
            logging.info("unregistration from '%s' done", msb_url)
        else:
            logging.info("unregistration from '%s' failed; status_code = '%s'", msb_url, resp.status_code)
    except:
        logging.info("unregistration from '%s' failed", msb_url)


if __name__ == '__main__':
    start_app(create_app())
