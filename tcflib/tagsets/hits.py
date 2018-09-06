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
The HiTS tagset mapped onto ISOcat DC-1345.

Dipper, S., Donhauser, K., Klein, T., Linde, S., Müller, S., & Wegera, K.-P.
(2013). HiTS: ein Tagset für historische Sprachstufen des Deutschen. Journal for
Language Technology and Computational Linguistics, Special Issue, 28(1), 85–137,
<http://www.jlcl.org/2013_Heft1/5Dipper.pdf>.

"""

from tcflib.tagsets.base import MappingTag, MappingTagSet, register_tagset
from tcflib.tagsets.dc1345 import POSTag, POSTagSet


class HiTag(MappingTag, POSTag):
    name2pid = {
        '$_': 'http://www.isocat.org/datcat/DC-2075',  # mainPunctuation; originale Interpunktion
        'ADJA': 'http://www.isocat.org/datcat/DC-1230',  # adjective; Adjektiv, attributiv, vorangestellt
        'ADJD': 'http://www.isocat.org/datcat/DC-1230',  # adjective; Adjektiv, prädikativ
        'ADJN': 'http://www.isocat.org/datcat/DC-1230',  # adjective; Adjektiv, attributiv, nachgestellt
        'ADJS': 'http://www.isocat.org/datcat/DC-1230',  # adjective; Adjektiv, substituierend
        'APPR': 'http://www.isocat.org/datcat/DC-1366',  # preposition; Präposition
        'AVD': 'http://www.isocat.org/datcat/DC-1232',  # adverb; Adverb
        'AVD-KO*':'http://www.isocat.org/datcat/DC-1232',  # adverb; Adverb oder Konjunktion
        'AVG': 'http://www.isocat.org/datcat/DC-1232',  # adverb; Relativadverb, generalisierend
        'AVW': 'http://www.isocat.org/datcat/DC-1232',  # adverb; Adverb, interrogativ
        'CARDA': 'http://www.isocat.org/datcat/DC-1334',  # numeral; Kardinalzahl, attributiv, vorangestellt
        'CARDD': 'http://www.isocat.org/datcat/DC-1334',  # numeral; Kardinalzahl, prädikativ
        'CARDN': 'http://www.isocat.org/datcat/DC-1334',  # numeral; Kardinalzahl, attributiv, nachgestellt
        'CARDS': 'http://www.isocat.org/datcat/DC-1334',  # numeral; Kardinalzahl, substituierend
        'DDA': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, definit, attributiv, vorangestellt
        'DDART': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, definit, artikelartig
        'DDD': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, definit/demonstrativ, prädikativ
        'DDN': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, definit/demonstrativ, attributiv, nachgestellt
        'DDS': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, definit/demonstrativ, substituierend
        'DGA': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, generalisierend, attributiv, vorangestellt
        'DGS': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, generalisierend, substituierend
        'DIA': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, indefinit, attributiv, vorangestellt
        'DIART': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, indefinit, artikelartig
        'DID': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, indefinit, prädikativ
        'DIN': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, indefinit, attributiv, nachgestellt
        'DIS': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, indefinit, substituierend
        'DPOSA': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, possessiv, attributiv, vorangestellt
        'DPOSD': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, possessiv, prädikativ
        'DPOSN': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, possessiv, attributiv, nachgestellt
        'DPOSS': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, possessiv, substituierend
        'DRELS': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, relativisch, substituierend
        'DWA': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, interrogativ, attributiv, vorangestellt
        'DWD': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, interrogativ, prädikativ
        'DWS': 'http://www.isocat.org/datcat/DC-1272',  # determiner; Determinativ, interrogativ, substituierend
        'FM': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual; Fremdsprachliches Material
        'ITJ': 'http://www.isocat.org/datcat/DC-1318',  # interjection; Interjektion
        'KO*': 'http://www.isocat.org/datcat/DC-1260',  # conjunction; Konjunktion, neben- oder unterordnend
        'KOKOM': 'http://www.isocat.org/datcat/DC-1922',  # comparativeParticle; Vergleichspartikel
        'KON': 'http://www.isocat.org/datcat/DC-1262',  # coordinatingConjunction; Konjunktion, nebenordnend
        'KOUS': 'http://www.isocat.org/datcat/DC-1393',  # subordinatingConjunction; Konjunktion, unterordnend
        'NA': 'http://www.isocat.org/datcat/DC-1371',  # properNoun; Nomen appelativum
        'NE': 'http://www.isocat.org/datcat/DC-1371',  # properNoun; Eigenname
        'PAVAP': 'http://www.isocat.org/datcat/DC-2998',  # pronominalAdverb; Pronominaladverb, präpositionaler Teil
        'PAVD': 'http://www.isocat.org/datcat/DC-2998',  # pronominalAdverb; Pronominaladverb, pronominaler Teil
        'PAVG': 'http://www.isocat.org/datcat/DC-2998',  # pronominalAdverb; Pronominaladverb, pronominaler Teil, generalisierend
        'PAVW': 'http://www.isocat.org/datcat/DC-2998',  # pronominalAdverb; Pronominaladverb, pronominaler Teil, interrogativ
        'PG': 'http://www.isocat.org/datcat/DC-1370',  # pronoun; Pronomen, generalisierend
        'PI': 'http://www.isocat.org/datcat/DC-1309',  # indefinitePronoun; Pronomen, indefinit
        'PPER': 'http://www.isocat.org/datcat/DC-3013',  # irreflexivePersonalPronoun; Pronomen, personal, irreflexiv
        'PRF': 'http://www.isocat.org/datcat/DC-3014',  # reflexivePersonalPronoun; Pronomen, personal, reflexiv
        'PTKA': 'http://www.isocat.org/datcat/DC-1922',  # comparativeParticle; Partikel bei Adjektiv oder Adverb
        'PTKANT': 'http://www.isocat.org/datcat/DC-1342',  # particle; Antwortpartikel
        'PTKNEG': 'http://www.isocat.org/datcat/DC-1894',  # negativeParticle; Negationspartikel
        'PTKVZ': 'http://www.isocat.org/datcat/DC-1342',  # particle; Verbzusatz
        'PW': 'http://www.isocat.org/datcat/DC-1321',  # interrogativePronoun; Pronomen, interrogativ
        'VAFIN': 'http://www.isocat.org/datcat/DC-1263',  # copula; Auxiliar, finit
        'VAIMP': 'http://www.isocat.org/datcat/DC-1263',  # copula; Auxiliar, Imperativ
        'VAINF': 'http://www.isocat.org/datcat/DC-1263',  # copula; Auxiliar, Infinitiv
        'VAPP': 'http://www.isocat.org/datcat/DC-1263',  # copula; Auxiliar, Partizip Präteritum, im Verbalkomplex
        'VAPS': 'http://www.isocat.org/datcat/DC-1263',  # copula; Auxiliar, Partizip Präsens, im Verbalkomplex
        'VMFIN': 'http://www.isocat.org/datcat/DC-1329',  # modal; Modalverb, finit
        'VMIMP': 'http://www.isocat.org/datcat/DC-1329',  # modal; Modalverb, Imperativ
        'VMINF': 'http://www.isocat.org/datcat/DC-1329',  # modal; Modalverb, Infinitiv
        'VMPP': 'http://www.isocat.org/datcat/DC-1329',  # modal; Modalverb, Partizip Präteritum, im Verbalkomplex
        'VMPS': 'http://www.isocat.org/datcat/DC-1329',  # modal; Modalverb, Partizip Präsens, im Verbalkomplex
        'VVFIN': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb; Vollverb, finit
        'VVIMP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb; Vollverb, Imperativ
        'VVINF': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb; Vollverb, Infinitiv
        'VVPP': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb; Partizip Präteritum, im Verbalkomplex
        'VVPS': 'http://www.isocat.org/datcat/DC-1400',  # mainVerb; Partizip Präsens, im Verbalkomplex
        '--': 'http://www.isocat.org/datcat/DC-1891',  # unclassifiedResidual
        }
    pid2name = {v: k for k, v in name2pid.items()}


class HiTagSet(MappingTagSet, POSTagSet):
    name = 'HiTS'
    tag_class = HiTag


register_tagset(HiTagSet)
