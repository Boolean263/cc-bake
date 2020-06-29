#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from pathlib import Path

import requests
import ccbake


def main():
    default_server = "localhost:3000"

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
        recipe = ccbake.Recipe(args.recipe)
    elif args.recipe_file:
        recipe = ccbake.Recipe(args.recipe_file.read())
    else:
        parser.error("Recipe option required: please specify " +
                     "--recipe or --recipe-file")

    out_fh = None
    out_dir = False
    if args.output == '-':
        # Write everything as binary to stdout
        out_fh = sys.stdout.buffer
    else:
        # Determine if output exists, and is a file or directory
        od = Path(args.output)
        if not od.exists() and args.output[-1] == os.sep:
            # Doesn't exist, but name ends with a '/',
            # which implies the user wanted a directory
            od.mkdir()
        if od.is_dir():
            # Exists and is a directory.
            out_dir = od

        if not out_dir:
            # If we don't have an output directory,
            # write all output to the given file name
            out_fh = open(args.output, "wb")

    try:
        for in_fh in args.infile:
            data = in_fh.read()
            result = ccbake.bake(args.server, recipe, data)
            if out_dir:
                in_name = Path(in_fh.name)
                out_name = out_dir.joinpath(in_name.name)
                out_fh = open(out_name, "wb")
            out_fh.write(result)
            if out_dir:
                out_fh.close()
            in_fh.close()
    except (
            requests.exceptions.ConnectionError,
            ccbake.BakeException,
    ) as e:
        sys.stderr.write("Bake error: {}\n".format(e))
        sys.exit(1)
    except (
        OSError,
    ) as e:
        sys.stderr.write("File I/O error: {}\n".format(e))
        sys.exit(1)


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
