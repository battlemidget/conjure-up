from conjureup.app_config import app
from contextlib import ContextDecorator


class step(ContextDecorator):
    def __init__(self, name, desc, result):
        self.name = name
        self.desc = desc
        self.result = result

    def __enter__(self):
        # app.log.debug("Running step: {}".format(self.desc))
        self.result = "testing step"

    def __exit__(self, *exc):
        # app.log.debug("Exiting step: {}".format(self.desc))
        return self.result
