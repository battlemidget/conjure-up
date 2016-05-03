from collections import OrderedDict
from ubuntui.widgets.input import StringEditor

""" Crafting schema
"""

Schema = OrderedDict([
    ('name', ('Package Name', StringEditor())),
    ('_version', "0.0.1"),
    ('_summary', "Enter a summary"),
    ('_excerpt', "Enter an excerpt"),
    ('_maintainer', 'Joe Bob <joe.bob@example.com>'),
    ('bundle',
     OrderedDict([
          ('name', ('Bundle Name', StringEditor())),
          ('summary', ('Bundle Summary', StringEditor()))
      ])
     )
])
