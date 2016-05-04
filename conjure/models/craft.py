from collections import OrderedDict
from ubuntui.widgets.input import StringEditor

""" Crafting schema
"""

Schema = OrderedDict([
    ('name', ('Package Name', StringEditor())),
    ('version', ('Version', StringEditor(default="0.0.1"))),
    ('summary', ('Summary', StringEditor(default="Amazing Solution"))),
    ('excerpt',
     ('Excerpt', StringEditor(
         default="Solutions for installing greatness"))),
     ('maintainer',
      ('Maintainer',
       StringEditor(default='Joe Bob <joe.bob@example.com>'))),
    ('bundle',
      OrderedDict([
          ('name', ('Bundle Name', StringEditor())),
          ('summary', ('Bundle Summary', StringEditor()))
      ])
     )
])
