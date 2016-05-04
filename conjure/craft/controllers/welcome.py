from conjure.craft.ui.views.welcome import WelcomeView
from conjure.utils import pollinate, spew
from conjure import template
from conjure.models.craft import Schema as CraftSchema
import json
import os


class WelcomeController:
    def __init__(self, app):
        self.app = app
        self.schema = CraftSchema
        self.view = WelcomeView(self.app,
                                self.schema,
                                self.finish)

    def _format_bundle(self, bundle):
        """ Formats bundle
        """
        name = bundle['name']
        key = bundle['name']
        summary = bundle['summary']
        return {
            'name': name,
            'key': key,
            'summary': summary
        }

    def _format_craftinput(self, craftitems):
        """ Formats the craft input into strings from the widgets values
        """
        formatted = {}
        for k, v in craftitems.items():
            if k == 'bundle':
                continue
            display, w = v
            formatted[k] = w.value
        bundle = self._format_bundle(craftitems['bundle'])
        formatted['bundles'] = [self._format_bundle(bundle)]
        return formatted

    def finish(self, items):
        """ Finalizes craft welcome screen

        Arguments:
        items: questionaire results
        """
        pollinate(self.app.session_id, 'C002', self.app.log)
        formatted = self._format_craftinput(items)

    def render(self):
        pollinate(self.app.session_id, 'C001', self.app.log)
        self.app.ui.set_header(
            title="Crafting a package"
        )
        self.app.ui.set_body(self.view)
