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


class STTag(MappingTag, POSTag):
    name2pid = {
        '$(': 'http://www.isocat.org/datcat/DC-1372',  # punctuation
        '$,': 'http://www.isocat.org/datcat/DC-2076',  # secondaryPunctuation
        '$.': 'http://www.isocat.org/datcat/DC-2075',  # mainPunctuation
        'ADJA': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'ADJD': 'http://www.isocat.org/datcat/DC-1230',  # adjective
        'ADV': 'http://www.isocat.org/datcat/DC-1232',  # adverb
        'APPO': 'http://www.isocat.org/datcat/DC-1360',  # postposition
        'APPR': 'http://www.isocat.org/datcat/DC-1366',  # preposition
        'APPRART': 'http://www.isocat.org/datcat/DC-3010',  # fusedPrepositionDeterminer
        'APZR': 'http://www.isocat.org/datcat/DC-1906',  # circumposition
        'ART': 'http://www.isocat.org/datcat/DC-1892',  # article
        'CARD': 'http://www.isocat.org/datcat/DC-1334',  # numeral
        'FM': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual
        'ITJ': 'http://www.isocat.org/datcat/DC-1318',  # interjection
        'KOKOM': 'http://www.isocat.org/datcat/DC-1922',  # comparativeParticle
        'KON': 'http://www.isocat.org/datcat/DC-1262',  # coordinatingConjunction
        'KOUI': 'http://www.isocat.org/datcat/DC-1393',  # subordinatingConjunction
        'KOUS': 'http://www.isocat.org/datcat/DC-1393',  # subordinatingConjunction
        'NE': 'http://www.isocat.org/datcat/DC-1371',  # properNoun
        'NN': 'http://www.isocat.org/datcat/DC-1333',  # noun
        'PDAT': 'http://www.isocat.org/datcat/DC-1270',  # demonstrativePronoun
        'PDS': 'http://www.isocat.org/datcat/DC-1270',  # demonstrativePronoun
        'PIAT': 'http://www.isocat.org/datcat/DC-1309',  # indefinitePronoun
        'PIDAT': 'http://www.isocat.org/datcat/DC-1309',  # indefinitePronoun
        'PIS': 'http://www.isocat.org/datcat/DC-1309',  # indefinitePronoun
        'PPER': 'http://www.isocat.org/datcat/DC-3013',  # irreflexivePersonalPronoun
        'PPOSAT': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'PPOSS': 'http://www.isocat.org/datcat/DC-1359',  # possessivePronoun
        'PRELAT': 'http://www.isocat.org/datcat/DC-1380',  # relativePronoun
        'PRELS': 'http://www.isocat.org/datcat/DC-1380',  # relativePronoun
        'PRF': 'http://www.isocat.org/datcat/DC-3014',  # reflexivePersonalPronoun
        'PROP': 'http://www.isocat.org/datcat/DC-2998',  # pronominalAdverb
        'PROAV': 'http://www.isocat.org/datcat/DC-2998',  # pronominalAdverb
        'PTKA': 'http://www.isocat.org/datcat/DC-1922',  # comparativeParticle
        'PTKANT': 'http://www.isocat.org/datcat/DC-1342',  # particle
        'PTKNEG': 'http://www.isocat.org/datcat/DC-1894',  # negativeParticle
        'PTKVZ': 'http://www.isocat.org/datcat/DC-1342',  # particle
        'PTKZU': 'http://www.isocat.org/datcat/DC-1896',  # infinitiveParticle
        'PWAT': 'http://www.isocat.org/datcat/DC-1321',  # interrogativePronoun
        'PWAV': 'http://www.isocat.org/datcat/DC-1380',  # relativePronoun
        'PWS': 'http://www.isocat.org/datcat/DC-1321',  # interrogativePronoun
        'TRUNC': 'http://www.isocat.org/datcat/DC-1897',  # unclassifiedParticle # FIXME
        'VAFIN': 'http://www.isocat.org/datcat/DC-1263',  # copula
        'VAIMP': 'http://www.isocat.org/datcat/DC-1263',  # copula
        'VAINF': 'http://www.isocat.org/datcat/DC-1263',  # copula
        'VAPP': 'http://www.isocat.org/datcat/DC-1263',  # copula
        'VMFIN': 'http://www.isocat.org/datcat/DC-1329',  # modal
        'VMINF': 'http://www.isocat.org/datcat/DC-1329',  # modal
        'VMPP': 'http://www.isocat.org/datcat/DC-1329',  # modal
        'VVFIN': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVIMP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVINF': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVIZU': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'VVPP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb
        'XY': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual
    }
    pid2name = {v: k for k, v in name2pid.items()}


class STTagSet(MappingTagSet, POSTagSet):
    name = 'STTS'
    tag_class = STTag


register_tagset(STTagSet)
