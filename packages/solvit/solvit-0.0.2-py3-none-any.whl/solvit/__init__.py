#!env python
# -*- coding: utf-8 -*-
"""
=======================================================================
:AUTHOR:	 Tralah M Brian <briantralah@tralahtek.com>
:TWITTER: 	 @TralahM <https://twitter.com/TralahM>
:GITHUB: 	 <https://github.com/TralahM>
:KAGGLE: 	 <https://kaggle.com/TralahM>
:COPYRIGHT:  (c) 2020  TralahTek LLC.
:LICENSE: 	 MIT , see LICENSE for more details.
:WEBSITE:	<https://www.tralahtek.com>
:CREATED: 	2020-06-30  06:58

:FILENAME:	__init__.py
=======================================================================


    DESCRIPTION OF SOLVIT PACKAGE:

SOLVIT
"""
from . import models
from argparse import ArgumentParser


__version__ = "1.0.0"


class Solvit:
    @staticmethod
    def puzzle_from_csv(filename):
        lst = []
        with open(filename, "r") as f:
            for ln in f.readlines():
                dat = ln.split(",")
                v = dat[:-1]
                t = int(dat[-1])
                lst.append(models.Expression(v, t))
        return models.Puzzle(lst)

    @staticmethod
    def puzzle_from_tsv(filename):
        lst = []
        with open(filename, "r") as f:
            for ln in f.readlines():
                dat = ln.split("\t")
                v = dat[:-1]
                t = int(dat[-1])
                lst.append(models.Expression(v, t))
        return models.Puzzle(lst)


def main():
    epilog = "Author: TralahM\n Email: <musyoki.brian@tralahtek.com>.\n Copyright:2020 (All Rights Reserved). "
    ps = ArgumentParser(
        description="Solvit Alphametic Puzzle Solver", epilog=epilog,)
    ps.add_argument(
        "-f",
        "--file",
        action="store",
        dest="filename",
        help="File containing solvit puzzle",
    )
    ps.add_argument(
        "-t",
        "--tsv",
        action="store_true",
        dest="tsv",
        default=False,
        help="is filetype tsv if not csv is assumed",
    )
    args = ps.parse_args()
    if args.tsv:
        puzzle = Solvit.puzzle_from_tsv(args.filename)
        puzzle.solve()
    else:
        puzzle = Solvit.puzzle_from_csv(args.filename)
        puzzle.solve()
