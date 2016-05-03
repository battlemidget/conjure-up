from collections import OrderedDict
from ubuntui.widgets.input import StringEditor

""" Crafting bundle schema
"""

Schema = OrderedDict([
    ('name', StringEditor()),
    ('key', StringEditor()),
    ('summary', StringEditor()),
    ('recommendedCharms', StringEditor()),
    ('bundleSeries', StringEditor(default='xenial')),
    ('whitelist', StringEditor()),
    ('location', StringEditor())
])
