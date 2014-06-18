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
The Stein tagset mapped onto ISOcat DC-1345.

"""

from tcflib.tagsets.base import MappingTag, MappingTagSet, register_tagset
from tcflib.tagsets.dc1345 import POSTag, POSTagSet


class SteinTag(MappingTag, POSTag):
    name2pid = {
        'ABR': 'http://www.isocat.org/datcat/DC-1897',  # unclassifiedParticle # FIXME
        'ADJ': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'ADV': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        'DET:ART': 'http://www.isocat.org/datcat/DC-1892',  # article
        'DET:POS': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'INT': 'http://www.isocat.org/datcat/DC-1318',  # interjection
        'KON': 'http://www.isocat.org/datcat/DC-1260',  # conjunction
        'NAM': 'http://www.isocat.org/datcat/DC-1371',  # properNoun
        'NOM': 'http://www.isocat.org/datcat/DC-1333',  # noun
        'NUM': 'http://www.isocat.org/datcat/DC-1334',  # numeral
        'PRO': 'http://www.isocat.org/datcat/DC-1370',  # pronoun
        'PRO:DEM': 'http://www.isocat.org/datcat/DC-1270',  # demonstrativePronoun
        'PRO:IND': 'http://www.isocat.org/datcat/DC-1309',  # indefinitePronoun
        'PRO:PER': 'http://www.isocat.org/datcat/DC-1463',  # personalPronoun
        'PRO:POS': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'PRO:REL': 'http://www.isocat.org/datcat/DC-1380',  # relativePronoun
        'PRP': 'http://www.isocat.org/datcat/DC-1366',  # preposition
        'PRP:det': 'http://www.isocat.org/datcat/DC-3010',  # fusedPrepositionDeterminer
        'PUN': 'http://www.isocat.org/datcat/DC-2076',  # secondaryPunctuation
        'PUN:cit': 'http://www.isocat.org/datcat/DC-1372',  # punctuation
        'SENT': 'http://www.isocat.org/datcat/DC-2075',  # mainPunctuation
        'SYM': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual
        'VER:cond': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:futu': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:impe': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:impf': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:infi': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:pper': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:ppre': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:pres': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:simp': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:subi': 'http://www.isocat.org/datcat/DC-1424',  # verb
        'VER:subp': 'http://www.isocat.org/datcat/DC-1424',  # verb
    }
    pid2name = {v: k for k, v in name2pid.items()}


class SteinTagSet(MappingTagSet, POSTagSet):
    name = 'Stein'
    tag_class = SteinTag


register_tagset(SteinTagSet)
