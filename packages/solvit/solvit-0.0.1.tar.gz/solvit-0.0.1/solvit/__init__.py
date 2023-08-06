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
