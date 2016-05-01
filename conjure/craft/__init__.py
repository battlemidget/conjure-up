""" conjure-craft - Package builder
"""

import argparse
import sys
import os
from conjure.shell import shell
from conjure import __version__ as VERSION


class CraftException(Exception):
    """ Error in crafting
    """
    pass


class Craft:
    def __init__(self, opts):
        """ init

        Arguments:
        opts: Options passed in from cli
        """
        if os.path.isdir(opts.spell):
            raise CraftException(
                "{} directory exists, please specify another.".format(
                    opts.spell)
            )

        shell('mkdir -p {}'.format(opts.directory))


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
