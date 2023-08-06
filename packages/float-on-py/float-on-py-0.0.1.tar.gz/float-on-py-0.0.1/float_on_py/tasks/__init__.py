from urllib.parse import urlencode

import requests

import float_on_py.config as config

api_prefix = config.api_prefix()

headers = {"Authorization": "Bearer {}".format(config.api_key())}


def get(id=None, project_id=None):

    filters = {'project_id': project_id}

    checked_filters = {k: v for k, v in filters.items() if v is not None}

    if id is None:
        url = api_prefix + '/tasks' + "?" + urlencode(checked_filters)
        print(url)
        r = requests.get(url, headers=headers)
    else:
        r = requests.get(api_prefix + '/tasks/' + str(id), headers=headers)
    return r.json()