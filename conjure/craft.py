""" conjure-craft entrypoint
"""

from conjure import utils
from conjure.app_config import app
from conjure.log import setup_logging
import argparse
import os
import sys


def parse_options(argv):
    parser = argparse.ArgumentParser(prog="conjure-craft")
    parser.add_argument('-d', '--debug', action='store_true',
                        dest='debug',
                        help='Enable debug logging.')

    subparsers = parser.add_subparsers(help='conjure-craft subcommands help')
    subparsers.add_parser('init',
                          help='Craft a new spell')
    subparsers.add_parser('publish', help='Publish spell to registry')
    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    if os.geteuid() == 0:
        utils.info("")
        utils.info("This should _not_ be run as root or with sudo.")
        utils.info("")
        sys.exit(1)

    # Application Config
    app.argv = opts
    app.log = setup_logging("conjure-up/craft",
                            opts.debug)

    app.env = os.environ.copy()
