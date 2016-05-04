from __future__ import unicode_literals
from urwid import (WidgetWrap, Text, Pile,
                   Columns, Filler)
from ubuntui.widgets.hr import HR
from ubuntui.widgets.text import Instruction
from ubuntui.widgets.buttons import (cancel_btn, confirm_btn)
from ubuntui.utils import Color, Padding
from ubuntui.ev import EventLoop
from conjure.utils import pollinate


class WelcomeView(WidgetWrap):
    def __init__(self, app, input_items, cb):
        self.app = app
        self.cb = cb
        self.input_items = input_items
        self.current_focus = 2
        _pile = [
            Padding.center_60(
                Instruction("Enter your package options:")),
            Padding.center_60(HR()),
            Padding.center_60(self.build_inputs()),
            Padding.line_break(""),
            Padding.center_20(self.buttons())
        ]
        super().__init__(Filler(Pile(_pile), valign="middle"))

    def _swap_focus(self):
        if self._w.body.focus_position == 2:
            self._w.body.focus_position = 4
        else:
            self._w.body.focus_position = 2

    def keypress(self, size, key):
        if key in ['tab', 'shift tab']:
            self._swap_focus()
        return super().keypress(size, key)

    def buttons(self):
        confirm = confirm_btn(on_press=self.submit)
        cancel = cancel_btn(on_press=self.cancel)

        buttons = [
            Color.button_primary(confirm, focus_map='button_primary focus'),
            Color.button_secondary(cancel, focus_map='button_secondary focus')
        ]
        return Pile(buttons)

    def build_inputs(self):
        items = []
        for k in self.input_items.keys():
            if k == 'bundle':
                continue
            display = self.input_items[k][0]
            col = Columns(
                [
                    ('weight', 0.5, Text(display, align='right')),
                    Color.string_input(self.input_items[k][1],
                                       focus_map='string_input focus')
                ], dividechars=1
            )
            items.append(col)
            items.append(Padding.line_break(""))
        for k in self.input_items['bundle'].keys():
            display = self.input_items['bundle'][k][0]
            col = Columns(
                [
                    ('weight', 0.5, Text(display, align='right')),
                    Color.string_input(self.input_items['bundle'][k][1],
                                       focus_map='string_input focus')
                ], dividechars=1
            )
            items.append(col)
            items.append(Padding.line_break(""))
        return Pile(items)

    def cancel(self, button):
        pollinate(self.app.session_id, 'C009', self.app.log)
        EventLoop.exit(0)

    def submit(self, result):
        self.cb(self.input_items)
