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
A service that converts TCF to the Mallet input format.

"""

from collections import Counter

from lxml import etree
from tcflib import tcf
from tcflib.tagsets import TagSet
from tcflib.service import ReplacingWorker, run_as_cli

# Use ISOcat/MAF as reference tagset.
ISOcat = TagSet('DC-1345')

# Create a filter that tests tokens for POS.
# `token` is a tcflib.tcf.TokenElement.
# `token.postag` is a tcflib.tagsets.ISOcatTag.
# `token.postag.is_a` queries the tagset hierarchy: "commonNoun" is_a "noun".
def posfilter(postags):
    def pfilter(token):
        for postag in postags:
            if token.postag.is_a(postag):
                return True
        return False
    return pfilter


class MalletExporter(ReplacingWorker):

    # Define configuration options. They work both as command line arguments:
    # ./tcf2mallet.py --spantype paragraph --postags "noun" "verb" "adjective"
    # and as GET parameters:
    # GET /tcf2mallet/?spantype=paragraph&postags=noun
    __options__ = {
        'spantype': '',
        'postags': [''],
    }

    def run(self, input_data):
        # ReplacingWorker gets XML input as raw data.
        # Parse XML input with tcf.parser to get additional API sugar.
        tree = etree.ElementTree(etree.fromstring(input_data,
                                 parser=tcf.parser))
        # Trees use the normal lxml API, e.g. for XPath queries.
        corpus = tree.xpath('/data:D-Spin/text:TextCorpus',
                            namespaces=tcf.NS)[0]
        # Use TagSet API for token filtering
        if self.options.postags[0]:
            postags = [ISOcat[postag] for postag in self.options.postags]
            tokenfilter = posfilter(postags)
        else:
            tokenfilter = lambda token: not token.postag.is_closed
        # Use lxml XPath API for specific queries.
        if self.options.spantype:
            textspans = tree.xpath('//text:textspan[@type = $type]',
                                   type=self.options.spantype,
                                   namespaces=tcf.NS)
        else:
            textspans = tree.xpath('//text:textspan',
                                   namespaces=tcf.NS)
        # Do the actual work. This mallet output uses lemma as token value.
        lang = corpus.get('lang', 'xx')
        output = []
        for i, span in enumerate(textspans, start=1):
            words = [str(token.lemma) for token in span.tokens
                     if tokenfilter(token)]
            output.append('{} {} {}\n'.format(i, lang, ' '.join(words)))
        # ReplacingWorker returns output as raw data.
        return ''.join(output).encode('utf8')


if __name__ == '__main__':
    run_as_cli(MalletWorker)
