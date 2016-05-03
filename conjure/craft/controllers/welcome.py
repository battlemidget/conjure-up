from conjure.craft.ui.views.welcome import WelcomeView
from conjure.utils import pollinate
from conjure.models.craft import Schema as CraftSchema


class WelcomeController:
    def __init__(self, app):
        self.app = app
        self.schema = CraftSchema
        self.view = WelcomeView(self.app,
                                self.schema,
                                self.finish)

    def finish(self, items):
        """ Finalizes craft welcome screen

        Arguments:
        items: questionaire results
        """

        pollinate(self.app.session_id, 'C002', self.app.log)
        import q
        q(items)

    def render(self):
        pollinate(self.app.session_id, 'C001', self.app.log)
        self.app.ui.set_header(
            title="Crafting a package"
        )
        self.app.ui.set_body(self.view)
