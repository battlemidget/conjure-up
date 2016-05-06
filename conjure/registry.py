""" Search spell registry """

import requests
import toml

with open('/etc/conjure-up.toml') as fp:
    etc = toml.loads(fp.read())


def _filter_result(registry, name):
    for i in registry['spells']:
        if name == i['name']:
            return i
    return False

def _get_registry():
    spell_rest_api = "{}{}".format(etc['registry']['spell_server'],
                                   etc['registry']['spell_registry_path'])
    res = requests.get(spell_rest_api)
    if res.ok:
        return res.json()
    else:
        return {}

def get_spell(name):
    registry = _get_registry()
    spell = _filter_result(registry, name)
    if spell:
        return spell
    return False
