#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse

import ccbake


def main():
    default_server = "localhost:5000"

    parser = argparse.ArgumentParser(
        prog="cc-bake",
        description="Process local data through a CyberChef server")
    parser.add_argument("-V", "--version",
                        action="version",
                        version="%(prog)s {0}".format(ccbake.__version__),
                        help="Show version and exit")
    parser.add_argument("-v", "--verbose",
                        action="count", default=0,
                        help="Increase verbosity")
    parser.add_argument("-s", "--server",
                        metavar="HOST:PORT",
                        type=str,
                        help="Host+port of CyberChef Server " +
                        "(default from CYBERCHEF_SERVER or " +
                        default_server + ")")
    parser.add_argument("-r", "--recipe",
                        metavar="STRING",
                        type=str,
                        help="Recipe string")
    parser.add_argument("-f", "--recipe-file",
                        metavar="FILE",
                        type=argparse.FileType(mode="rt"),
                        help="Recipe file")
    parser.add_argument("-o", "--output",
                        metavar="FILE_OR_DIR",
                        type=str,
                        default='-',
                        help="Where to write output (default:stdout)")
    parser.add_argument("infile",
                        metavar="INFILE",
                        nargs="*",
                        type=argparse.FileType(mode="rb"),
                        default=[sys.stdin.buffer],
                        help="Read data from (default:stdin)")

    args = parser.parse_args()
    recipe = None

    if not args.server:
        try:
            args.server = os.environ['CYBERCHEF_SERVER']
        except KeyError:
            args.server = default_server

    if args.recipe and args.recipe_file:
        parser.error("Conflicting options specified: " +
                     "--recipe and --recipe-file")
    elif args.recipe:
        recipe = args.recipe
    elif args.recipe_file:
        recipe = args.recipe_file.read()
    else:
        parser.error("Recipe option required: please specify " +
                     "--recipe or --recipe-file")

    print("infiles={0}".format(args.infile))


if __name__ == '__main__':
    sys.exit(main() or 0)

# Editor modelines - http://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf-8
# End:
#
# vi:set shiftwidth=4 tabstop=4 expandtab fileencoding=utf-8:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf-8:
