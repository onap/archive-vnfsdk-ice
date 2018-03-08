import io
import json
import os
import sys

import pytest

#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Make sure that the application source directory (this directory's parent) is
# on sys.path.
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)
print(sys.path)

import app as myapp

ICE_URL = '/onapapi/ice/v1/'

flask_app = myapp.create_test_app()


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_404(client):
    response = client.get('/dummy')
    assert response.status_code == 404


def test_ping(client):
    response = client.get(ICE_URL, content_type='application/json')
    assert response.status_code == 200


def test_validate_nofile(client):
    response = client.post(ICE_URL)
    assert response.status_code == 400
    assert json_of_response(response) is not None


def test_validate_not_zip(client):
    data = {'file': (io.BytesIO(b'my file contents'), 'hello world.txt')}
    response = client.post(ICE_URL, data=data)
    assert response.status_code == 422


@pytest.mark.skip(reason="no way of currently testing this")
def test_validate_bad_zip(client):
    zf = os.path.join(os.path.dirname(__file__), 'fixture/test.zip')
    data = {'file': (zf, 'test.zip')}
    response = client.post(ICE_URL, data=data)
    print("##"+zf)
    assert response.status_code == 200


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
