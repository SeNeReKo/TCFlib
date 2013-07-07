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
The STTS tagset as modeled in ISOcat DC-2446.

"""

import os

from lxml import etree

from tcflib.tagsets.base import POSTagSetBase, POSTagBase, register_tagset, NS


class STTag(POSTagBase):
    # See http://www.sfs.uni-tuebingen.de/Elwis/stts/Wortlisten/WortFormen.html
    CLOSED = [
        'http://www.isocat.org/datcat/DC-3036',  # $(
        'http://www.isocat.org/datcat/DC-3034',  # $,
        'http://www.isocat.org/datcat/DC-3035',  # $.
        'http://www.isocat.org/datcat/DC-2838',  # APPO
        'http://www.isocat.org/datcat/DC-2836',  # APPR
        'http://www.isocat.org/datcat/DC-2837',  # APPRART
        'http://www.isocat.org/datcat/DC-2839',  # APZR
        'http://www.isocat.org/datcat/DC-2451',  # ART
        'http://www.isocat.org/datcat/DC-2871',  # KOKOM
        'http://www.isocat.org/datcat/DC-2870',  # KON
        'http://www.isocat.org/datcat/DC-2847',  # KOUI
        'http://www.isocat.org/datcat/DC-2848',  # KOUS
        'http://www.isocat.org/datcat/DC-2887',  # PROP
        'http://www.isocat.org/datcat/DC-2874',  # PDAT
        'http://www.isocat.org/datcat/DC-2873',  # PDS
        'http://www.isocat.org/datcat/DC-2876',  # PIAT
        'http://www.isocat.org/datcat/DC-2877',  # PIDAT
        'http://www.isocat.org/datcat/DC-2875',  # PIS
        'http://www.isocat.org/datcat/DC-2878',  # PPER
        'http://www.isocat.org/datcat/DC-2880',  # PPOSAT
        'http://www.isocat.org/datcat/DC-2879',  # PPOSS
        'http://www.isocat.org/datcat/DC-2882',  # PRELAT
        'http://www.isocat.org/datcat/DC-2881',  # PRELS
        'http://www.isocat.org/datcat/DC-2883',  # PRF
        'http://www.isocat.org/datcat/DC-2892',  # PTKA
        'http://www.isocat.org/datcat/DC-2891',  # PTKANT
        'http://www.isocat.org/datcat/DC-2889',  # PTKNEG
        'http://www.isocat.org/datcat/DC-2890',  # PTKVZ
        'http://www.isocat.org/datcat/DC-2888',  # PTKZU
        'http://www.isocat.org/datcat/DC-2885',  # PWAT
        'http://www.isocat.org/datcat/DC-2886',  # PWAV
        'http://www.isocat.org/datcat/DC-2884',  # PWS
        'http://www.isocat.org/datcat/DC-2899',  # VAFIN
        'http://www.isocat.org/datcat/DC-2900',  # VAIMP
        'http://www.isocat.org/datcat/DC-2901',  # VAINF
        'http://www.isocat.org/datcat/DC-2902',  # VAPP
        'http://www.isocat.org/datcat/DC-2903',  # VMFIN
        'http://www.isocat.org/datcat/DC-2904',  # VMINF
        'http://www.isocat.org/datcat/DC-2905',  # VMPP
        'http://www.isocat.org/datcat/DC-2906',  # XY
        ]
    _name_xpath = etree.XPath('string(dcif:descriptionSection/'
        'dcif:dataElementNameSection/'
        'dcif:dataElementName[1])',
        namespaces=NS)


class STTagSet(POSTagSetBase):
    __file__ = os.path.join(os.path.dirname(__file__),
                            'data', 'dc-2446.dcif')
    name = 'DC-2446'
    pid = 'http://www.isocat.org/datcat/DC-2446'
    tag_class = STTag

    _by_name_xpath = etree.XPath('//dcif:dataCategory['
        'dcif:descriptionSection/'
        'dcif:dataElementNameSection/'
        'dcif:dataElementName = $name][1]',
        namespaces=NS)


register_tagset(STTagSet)
