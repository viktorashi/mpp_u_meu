from mpp_backend import create_app
import json

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

