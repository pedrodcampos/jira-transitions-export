from os import path
import json
import sys


def load_config():
    filename = path.join(path.curdir, '.config.json')
    if path.isfile(filename):
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
            if set(config.keys()).issuperset(
                ['DOMAIN', 'USERNAME', "PASSWORD"]
            ) and all(config.values()):
                return config


def build_jira_config(domain=None, username=None, password=None):
    environ = load_config()
    return {"domain": domain if domain else environ.get('DOMAIN', None),
            "auth": (
            username
            if username else environ.get('USERNAME', None),
            password
            if password else environ.get('PASSWORD', None))
            }
