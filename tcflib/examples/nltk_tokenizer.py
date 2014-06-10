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

from nltk import sent_tokenize, word_tokenize

from tcflib.tcf import P_TEXT, Element, SubElement
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
            result.append(sourcelist[start:])
            break
    return result


class NltkTokenizer(AddingWorker):

    def add_annotations(self):
        # Add base elements
        tokens_elem = SubElement(self.corpus, P_TEXT + 'tokens')
        sentences_elem = SubElement(self.corpus, P_TEXT + 'sentences')
        structure_elem = SubElement(self.corpus, P_TEXT + 'textstructure')
        # Parse text
        #text = self.corpus.text.text
        text = self.corpus.find(P_TEXT + 'text').text
        paragraphs = listsplit(text.splitlines(), '')
        paragraphs = ['\n'.join(lines) for lines in paragraphs]
        i = -1
        j = -1
        for paragraph in paragraphs:
            par_word_ids = []
            for i, sentence in enumerate(sent_tokenize(paragraph),
                                         start=i + 1):
                sent_word_ids = []
                for j, word in enumerate(word_tokenize(sentence),
                                         start=j + 1):
                    word_id = 't_{}'.format(j)
                    sent_word_ids.append(word_id)
                    token_elem = SubElement(tokens_elem, P_TEXT + 'token',
                                                         ID=word_id)
                    token_elem.text = word
                par_word_ids.extend(sent_word_ids)
                sentence_elem = SubElement(sentences_elem, P_TEXT + 'sentence',
                                           ID='s_{}'.format(i),
                                           tokenIDs=' '.join(sent_word_ids))
            if not par_word_ids:
                # Empty paragraph
                continue
            span_elem = SubElement(structure_elem, P_TEXT + 'textspan',
                                   start=par_word_ids[0], end=par_word_ids[-1],
                                   type='paragraph')

if __name__ == '__main__':
    run_as_cli(NltkTokenizer)    
