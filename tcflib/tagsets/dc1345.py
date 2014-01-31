#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Frederik Elwert <frederik.elwert@web.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A POS tagset based on ISOcat DC-1345.

"""

import os

from tcflib.tagsets.base import POSTagSetBase, POSTagBase, register_tagset


class POSTag(POSTagBase):
    # See http://www.sfs.uni-tuebingen.de/Elwis/stts/Wortlisten/WortFormen.html
    CLOSED = [
        'http://www.isocat.org/datcat/DC-1372',  # punctuation
        'http://www.isocat.org/datcat/DC-1231',  # adposition
        'http://www.isocat.org/datcat/DC-1892',  # article
        'http://www.isocat.org/datcat/DC-1342',  # particle
        'http://www.isocat.org/datcat/DC-1260',  # conjunction
        'http://www.isocat.org/datcat/DC-2998',  # pronominal adverb
        'http://www.isocat.org/datcat/DC-1370',  # pronoun
        'http://www.isocat.org/datcat/DC-1263',  # copula
        'http://www.isocat.org/datcat/DC-1329',  # modal
        'http://www.isocat.org/datcat/DC-1891',  # unclassified residual
        'http://www.isocat.org/datcat/DC-1908',  # unspecified
        ]


class POSTagSet(POSTagSetBase):
    __file__ = os.path.join(os.path.dirname(__file__),
                            'data', 'dc-1345.dcif')
    name = 'DC-1345'
    pid = 'http://www.isocat.org/datcat/DC-1345'
    tag_class = POSTag


register_tagset(POSTagSet)
