#!flask/bin/python
import argparse
import logging
import requests

import connexion
from connexion.resolver import RestyResolver


def parse_args():
    """
    parse argument parameters
    """
    parser = argparse.ArgumentParser(description='start the heat validation rest server')
    parser.add_argument("--debug", help="increase output verbosity")
    parser.add_argument("-p", "--port", type=int, help="listen port (default 5000)", default=5000)
    args = parser.parse_args()
    if args.debug:
        logging.info("debug mode")
        debug = True
    else:
        debug = False
    if args.port:
        port = args.port
    else:
        port = 5000


def create_app():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = connexion.App(__name__, specification_dir='swagger/')

    # load default config
    app.app.config.from_object("default_settings")
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
    app.run(port=app.app.config['ICE_PORT'], debug=app.app.config['DEBUG'])

    # register service in MSB
    try:
        msb_url = app.app.config['MSB_URL']
        requests.get(msb_url)
        logging.info("registration to %s done", msb_url)
    except:
        logging.info("registration to %s failed", msb_url)


if __name__ == '__main__':
    start_app(create_app())
