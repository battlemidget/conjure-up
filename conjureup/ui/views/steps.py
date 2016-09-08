from urwid import Filler, Pile, WidgetWrap

from ubuntui.utils import Padding
from ubuntui.widgets.hr import HR


class StepsView(WidgetWrap):

    def __init__(self, app, steps, cb=None):
        """ init

        Arguments:
        cb: process step callback
        """
        self.app = app
        self.cb = cb
        self.steps = steps
        self.step_pile = Pile(
            [Padding.center_90(HR()),
             Padding.line_break("")] +
            [Padding.center_90(s) for s in self.steps] +
            [Padding.line_break(""),
             Padding.center_20(self.buttons())]
        )
        super().__init__(Filler(self.step_pile, valign="top"))

    def get_step_widget(self, index):
        return self.step_pile[index + 2]
