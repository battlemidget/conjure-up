""" conjure-craft - Package builder
"""

import argparse
import sys
import os
from conjure.shell import shell
from conjure import async
from ubuntui.ev import EventLoop
from ubuntui.palette import STYLES
from conjure.ui import ConjureUI
from conjure import __version__ as VERSION
from conjure.log import setup_logging


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


class Craft:
    def __init__(self, opts):
        """ init

        Arguments:
        opts: Options passed in from cli
        """
        self.app = CraftConfig(opts)

        if os.path.isdir(opts.spell):
            raise CraftException(
                "{} directory exists, please specify another.".format(
                    opts.spell)
            )

        shell('mkdir -p {}'.format(opts.directory))

    def unhandled_input(self, key):
        if key in ['q', 'Q']:
            async.shutdown()
            EventLoop.exit(0)


    def _start(self, *args, **kwargs):
        self.app.log.info("conjure-craft starting")
        async.shutdown()
        EventLoop.exit(0)

    def start(self):
        EventLoop.build_loop(self.app.ui, STYLES,
                             unhandled_input=self.unhandled_input)
        EventLoop.set_alarm_in(0.05, self._start)
        EventLoop.run()


def parse_options(argv):
    parser = argparse.ArgumentParser(description="Conjure craft",
                                     prog="conjure-craft")
    parser.add_argument('spell', help='Name of Juju solution to create')
    parser.add_argument('-d', '--debug', action='store_true',
                        dest='debug',
                        help='Enable debug logging.')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {}'.format(VERSION))
    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    if not opts.spell:
        raise CraftException(
            "A solution name is required."
        )

    try:
        Craft(opts)
        sys.exit(0)
    except CraftException as e:
        print(e)
        sys.exit(1)
