#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import base64
import copy
from collections import namedtuple as _namedtuple

import requests

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))


def namedtuple(typename, field_names, defaults=None):
    """\
    version-portable namedtuple with defaults, adapted from
    https://stackoverflow.com/a/18348004/6692652
    """
    if not defaults:
        # No defaults given or needed
        return _namedtuple(typename, field_names)
    try:
        # Python 3.7+
        return _namedtuple(typename, field_names, defaults=defaults)
    except TypeError:
        T = _namedtuple(typename, field_names)
        try:
            # Python 2.7, up to 3.6
            T.__new__.__defaults__ = defaults
        except AttributeError:
            # Older Python 2.x
            T.__new__.func_defaults = defaults
        return T


class Operation(object):
    """\
    A single operation within a recipe.
    Currently not used.
    """

    __slots__ = ['op', 'args']

    def __init__(self, op, args=None):
        """\
        Create a new Operation. Will eventually handle "Chef format"
        function-style operations.
        """
        if type(op) == dict:
            # We got a dict.
            # 'op' key is required; let this throw KeyError if needed
            self.op = op['op']
            try:
                # 'args' may not exist
                self.args = op['args']
            except KeyError:
                pass
        elif '(' in op:
            # Chef-format. Worry about this after I get JSON working
            raise NotImplemented
        else:
            # Plain string
            self.op = op
            self.args = args

    def __repr__(self):
        rv = {'op': self.op}
        # CyberChef can act weird if args is present but empty.
        # So, we only populate it if it's not empty.
        if not (self.args is None or len(self.args) == 0):
            rv['args'] = self.args
        return rv


class BakeException(Exception):
    pass


class Recipe(list):
    """\
    Recipe, as a list of individual operations.
    """

    def __init__(self, recipe):
        try:
            # Start assuming a JSON string
            item = json.loads(recipe)
            if type(item) != list:
                item = [item]
            list.__init__(self, item)
        except json.JSONDecodeError as e:
            # Not JSON. Maybe Chef-format? For now we can't handle that
            raise e


def bake(server, recipe, data):
    """\
    Send the data to the given server for processing. Return the result.
    """

    # Insulate the data for transmission as a string
    d = base64.b64encode(data).decode()
    r = copy.copy(recipe)
    r.insert(0, {'op': 'From Base64'})
    r.append({'op': 'To Base64'})

    req = requests.post("http://"+server+"/bake",
                        json={'input': d, 'recipe': r})

    if req.status_code == 200:
        return base64.b64decode(req.json()['value'])
    else:
        raise BakeException(req.text)


# Self-test code
if __name__ == '__main__':
    recipe_json = """
[
  { "op": "To Lower case",
    "args": [] },
  { "op": "Reverse",
    "args": ["Character"] }
]
"""
    # { "op": "ADD",
    # "args": [{ "option": "Hex", "string": "5" }] }

    r = Recipe(recipe_json)
    d = b"HELLO THERE"
    resp = bake("localhost:3000", r, d)

    print(resp)

#
# Editor modelines - http://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# End:
#
# vi:set shiftwidth=4 tabstop=4 expandtab:
# indentSize=4:tabSize=4:noTabs=true:
