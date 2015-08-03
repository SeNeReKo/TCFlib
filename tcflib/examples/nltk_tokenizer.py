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
A TCF tokenizer based on NLTK.

This tokenizer supports word tokenization as well as sentence and textstructure
detection.

"""

from nltk import sent_tokenize
from nltk.tokenize import wordpunct_tokenize as word_tokenize

from tcflib.tcf import (P_TEXT, Tokens, Token, Sentences, Sentence,
                        TextStructure, TextSpan)
from tcflib.service import AddingWorker, run_as_cli


def listsplit(sourcelist, delimiter):
    """
    Splits a list at a given delimiter. Returns a list of lists.

    Example:
    >>> l = ['a', '', 'b', 'c', '', '', 'd']
    >>> listsplit(l, '')
    [['a'], ['b', 'c'], ['d']]

    """
    result = []
    start = 0
    while True:
        try:
            position = sourcelist.index(delimiter, start)
            if start == position:
                start += 1
                continue
            result.append(sourcelist[start:position])
            start = position + 1
        except ValueError:
            tail = sourcelist[start:]
            if tail:
                result.append(tail)
            break
    return result


class NltkTokenizer(AddingWorker):

    def add_annotations(self):
        # Add base layers
        self.corpus.add_layer(Tokens())
        self.corpus.add_layer(Sentences())
        self.corpus.add_layer(TextStructure())
        # Parse text
        text = self.corpus.text.text
        paragraphs = listsplit(text.splitlines(), '')
        paragraphs = ['\n'.join(lines) for lines in paragraphs]
        for paragraph in paragraphs:
            textspan = TextSpan(type='paragraph')
            for sent in sent_tokenize(paragraph):
                sentence = Sentence()
                for word in word_tokenize(sent):
                    token = Token(word)
                    self.corpus.tokens.append(token)
                    sentence.tokens.append(token)
                    textspan.tokens.append(token)
                self.corpus.sentences.append(sentence)
            self.corpus.textstructure.append(textspan)

if __name__ == '__main__':
    run_as_cli(NltkTokenizer)    
