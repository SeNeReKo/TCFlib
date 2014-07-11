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
import re

from lxml import etree
from tcflib import tcf
from tcflib.tagsets import TagSet
from tcflib.service import ExportingWorker, run_as_cli

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


class MalletExporter(ExportingWorker):

    # Define configuration options. They work both as command line arguments:
    # ./tcf2mallet.py --spantype paragraph --postags "noun" "verb" "adjective"
    # and as GET parameters:
    # GET /tcf2mallet/?spantype=paragraph&postags=noun
    __options__ = {
        'spantype': '',
        'postags': [''],
        'prefix': ''
    }
    layers = ['tokens', 'POStags', 'lemmas', 'textstructure']

    def export(self):
        # ExportingWorker just has to override `export()` to return the target
        # Format as bytes. It can access `self.corpus` like an `AddingWorker`.
        # Use TagSet API for token filtering
        if self.options.postags[0]:
            postags = [ISOcat[postag] for postag in self.options.postags]
            tokenfilter = posfilter(postags)
        else:
            tokenfilter = lambda token: not token.postag.is_closed
        # The textstructure layer can be used like a list:
        if self.options.spantype:
            textspans = [span for span in self.corpus.textstructure
                         if span.type == self.options.spantype]
        else:
            textspans = self.corpus.textstructure
        # Ensure prefix does not contain whitespace
        prefix = re.sub(r'\s+', '_', self.options.prefix)
        # Do the actual work. This mallet output uses lemma as token value.
        output = []
        for i, span in enumerate(textspans, start=1):
            # Filter tokens by POS and use lemmata
            words = [token.lemma for token in span.tokens
                     if tokenfilter(token)]
            # Deal with TreeTagger’s `<unknown>` pseudo-lemma
            words = [word for word in words if not word == '<unknown>']
            # Append a line in mallet’s `<document> <label> <words...>` format
            output.append('{}{} {} {}\n'.format(prefix, i,
                                                self.corpus.lang,
                                                ' '.join(words)))
        # ExportingWorker returns output as bytes.
        return ''.join(output).encode('utf8')


if __name__ == '__main__':
    run_as_cli(MalletWorker)
