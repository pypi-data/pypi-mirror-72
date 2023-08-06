import requests
import float_on_py.config as config

api_prefix = config.api_prefix()

headers = {"Authorization": "Bearer {}".format(config.api_key())}


def get(id=None):

    if id is None:
        r = requests.get(api_prefix + '/clients', headers=headers)
    else:
        r = requests.get(api_prefix + '/clients/' + str(id), headers=headers)
    return r.json()