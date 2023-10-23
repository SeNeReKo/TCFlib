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
The STTS tagset mapped onto ISOcat DC-1345.

"""

from tcflib.tagsets.base import MappingTag, MappingTagSet, register_tagset
from tcflib.tagsets.dc1345 import POSTag, POSTagSet


class UDTag(MappingTag, POSTag):
    # See https://universaldependencies.org/u/pos/
    CLOSED = [
        'http://www.isocat.org/datcat/DC-1231',
        'http://www.isocat.org/datcat/DC-1244',
        'http://www.isocat.org/datcat/DC-1262',
        'http://www.isocat.org/datcat/DC-1272',
        'http://www.isocat.org/datcat/DC-1334',
        'http://www.isocat.org/datcat/DC-1342',
        'http://www.isocat.org/datcat/DC-1370',
        'http://www.isocat.org/datcat/DC-1393',
        'http://www.isocat.org/datcat/DC-1372',
    ]
    name2pid = {
        'ADJ': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'ADP': 'http://www.isocat.org/datcat/DC-1231',  # adposition
        'ADV': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        'AUX': 'http://www.isocat.org/datcat/DC-1244',  # auxiliary
        'CCONJ': 'http://www.isocat.org/datcat/DC-1262',  # coordinating conjunction
        'DET': 'http://www.isocat.org/datcat/DC-1272',  # determiner
        'INTJ': 'http://www.isocat.org/datcat/DC-1318',  # interjection
        'NOUN': 'http://www.isocat.org/datcat/DC-1333',  # noun
        'NUM': 'http://www.isocat.org/datcat/DC-1334',  # numeral
        'PART': 'http://www.isocat.org/datcat/DC-1342',  # particle
        'PRON': 'http://www.isocat.org/datcat/DC-1370',  # pronoun
        'PROPN': 'http://www.isocat.org/datcat/DC-1371',  # proper noun
        'PUNCT': 'http://www.isocat.org/datcat/DC-1372',  # punctuation
        'SCONJ': 'http://www.isocat.org/datcat/DC-1393',  # subordinating conjunction
        'SYM': 'http://www.isocat.org/datcat/DC-1398',  # symbol
        'VERB': 'http://www.isocat.org/datcat/DC-1400',  # verb
        'X': 'http://www.isocat.org/datcat/DC-1891',  # other
    }
    pid2name = {v: k for k, v in name2pid.items()}


class UDTagSet(MappingTagSet, POSTagSet):
    name = 'UD'
    tag_class = UDTag


register_tagset(UDTagSet)
