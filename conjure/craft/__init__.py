""" conjure-craft - Package builder
"""

import argparse
import sys
import os
import uuid
import string
from conjure.shell import shell
from conjure import async
from ubuntui.ev import EventLoop
from ubuntui.palette import STYLES
from conjure.ui import ConjureUI
from conjure import __version__ as VERSION
from conjure.log import setup_logging
from conjure.craft.controllers.welcome import WelcomeController

class CraftException(Exception):
    """ Error in crafting
    """
    pass


class CraftConfig:
    """ Craft configuration persisted throughout the entire
    life of the application """

    def __init__(self, argv):
        self.ui = ConjureUI()
        self.argv = argv
        self.env = os.environ.copy()
        self.log = setup_logging('conjure-craft',
                                 self.argv.debug)
        self.package = argv.name
        self.bundle = argv.bundle

        self.controllers = None
        # Global session id
        self.session_id = os.getenv('CONJURE_TEST_SESSION_ID',
                                    str(uuid.uuid4()))


class Craft:
    def __init__(self, opts):
        """ init

        Arguments:
        opts: Options passed in from cli
        """
        self.app = CraftConfig(opts)
        self.app.controllers = {
            'welcome': WelcomeController(self.app)
        }

    def unhandled_input(self, key):
        if key in ['q', 'Q']:
            async.shutdown()
            EventLoop.exit(0)

    def _start(self, *args, **kwargs):
        self.app.log.info("conjure-craft starting")
        self.app.controllers['welcome'].render()

    def start(self):
        EventLoop.build_loop(self.app.ui, STYLES,
                             unhandled_input=self.unhandled_input)
        EventLoop.set_alarm_in(0.05, self._start)
        EventLoop.run()


def parse_options(argv):
    parser = argparse.ArgumentParser(description="Conjure craft",
                                     prog="conjure-craft")
    parser.add_argument('name', help='Name of the package')
    parser.add_argument('bundle', help='Bundle file to package')
    parser.add_argument('-d', '--debug', action='store_true',
                        dest='debug',
                        help='Enable debug logging.')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {}'.format(VERSION))
    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    if not opts.name:
        print("A package name is required")
        sys.exit(1)

    if len(set(string.punctuation) & set(opts.name)) > 0:
        print("Package must not contain {}".format(string.punctuation))
        sys.exit(1)

    if os.path.isdir(opts.name):
        print("Directory already exists for package name, "
              "please choose another or move to another directory.")
        sys.exit(1)
    else:
        os.makedirs(opts.name)

    if not opts.bundle:
        print("A bundle is required.")
        sys.exit(1)
    if not os.path.isfile(opts.bundle):
        print("Unable to locate bundle file.")
        sys.exit(1)

    try:
        app = Craft(opts)
        sys.exit(app.start())
    except CraftException as e:
        print(e)
        sys.exit(1)
