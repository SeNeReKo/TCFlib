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
The Penn treebank tagset mapped onto ISOcat DC-1345.

"""

from tcflib.tagsets.base import MappingTag, MappingTagSet, register_tagset
from tcflib.tagsets.dc1345 import POSTag, POSTagSet


class PennTag(MappingTag, POSTag):
    name2pid = {
        'CC': 'http://www.isocat.org/datcat/DC-1262',  # coordinatingConjunction
        'CD': 'http://www.isocat.org/datcat/DC-1334',  # numeral
        'DT': 'http://www.isocat.org/datcat/DC-1272',  # determiner
        'EX': 'http://www.isocat.org/datcat/DC-1917',  # particleAdverb FIXME
        'FW': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual
        'IN': 'http://www.isocat.org/datcat/DC-1393',  # subordinatingConjunction
        'JJ': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'JJR': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'JJS': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'LS': 'http://www.isocat.org/datcat/DC-1438',  # bullet
        'MD': 'http://www.isocat.org/datcat/DC-1329',  # modal
        'NN': 'http://www.isocat.org/datcat/DC-1333',  # noun
        'NNS': 'http://www.isocat.org/datcat/DC-1333',  # noun
        'NNP': 'http://www.isocat.org/datcat/DC-1371',  # properNoun
        'NNPS': 'http://www.isocat.org/datcat/DC-1371',  # properNoun
        'PDT': 'http://www.isocat.org/datcat/DC-1272',  # determiner FIXME
        'POS': 'http://www.isocat.org/datcat/DC-1895',  # possessiveParticle
        'PRP': 'http://www.isocat.org/datcat/DC-1463',  # personalPronoun
        'PRP$': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'RB': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        'RBR': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        'RBS': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        'RP': 'http://www.isocat.org/datcat/DC-1917',  # particleAdverb
        'SYM': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual FIXME
        'TO': 'http://www.isocat.org/datcat/DC-1896',  # infinitiveParticle
        'UH': 'http://www.isocat.org/datcat/DC-1318',  # interjection
        'VB': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VBZ': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VBP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VBN': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VBG': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'WDT': 'http://www.isocat.org/datcat/DC-1272',  # determiner
        'WP': 'http://www.isocat.org/datcat/DC-1463',  # personalPronoun
        'WP$': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'WRB': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        '.': 'http://www.isocat.org/datcat/DC-2075',  # mainPunctuation
        ',': 'http://www.isocat.org/datcat/DC-2076',  # secondaryPunctuation
        ':': 'http://www.isocat.org/datcat/DC-1439',  # colon
        #'(': 'http://www.isocat.org/datcat/DC-2078',  # openPunctuation  FIXME: Not in dcif data
        #')': 'http://www.isocat.org/datcat/DC-2079',  # closePunctuation  FIXME: Not in dcif data
        '(': 'http://www.isocat.org/datcat/DC-2076',  # secondaryPunctuation
        ')': 'http://www.isocat.org/datcat/DC-2076',  # secondaryPunctuation
        ## additional tags
        'VBD': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VH': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VHD': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VHG': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VHN': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VHP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VHZ': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VV': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVD': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVG': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVN': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVZ': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'PP': 'http://www.isocat.org/datcat/DC-1463',  # personalPronoun
        'PP$': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'NP': 'http://www.isocat.org/datcat/DC-1371',  # properNoun
        'NPS': 'http://www.isocat.org/datcat/DC-1371',  # properNoun
        'SENT': 'http://www.isocat.org/datcat/DC-2075',  # mainPunctuation
        'IN/that': 'http://www.isocat.org/datcat/DC-1393',  # subordinatingConjunction
        '``': 'http://www.isocat.org/datcat/DC-2076',  # secondaryPunctuation  FIXME
    }
    pid2name = {v: k for k, v in name2pid.items()}


class PennTagSet(MappingTagSet, POSTagSet):
    name = 'PennTB'
    tag_class = PennTag


register_tagset(PennTagSet)
