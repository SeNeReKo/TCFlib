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
This module provides an API for TCF documents.

"""

from collections import UserList, UserDict, OrderedDict
from warnings import warn

from lxml import etree

from tcflib.tagsets import TagSet

NS_DATA = 'http://www.dspin.de/data'
P_DATA = '{' + NS_DATA + '}'
NS_TEXT = 'http://www.dspin.de/data/textcorpus'
P_TEXT = '{' + NS_TEXT + '}'
NS = {'data': NS_DATA, 'text': NS_TEXT}


class AnnotationLayer(UserList):

    element = ''

    @property
    def tcf(self):
        elem = etree.Element(P_TEXT + self.element)
        for child in self.data:
            elem.append(child.tcf)


class AnnotationLayerWithIDs(UserDict):

    element = ''

    def __init__(self, initialdata=None):
        self.data = OrderedDict()
        if initialdata:
            self.data.update(initialdata)

    def __iter__(self):
        return iter(self.data.values())

    def __setitem__(self, key, item):
        item.parent = self
        self.data[key] = item

    def keys(self):
        return self.data.keys()

    def append(self, item):
        item.parent = self
        key = '{}_{}'.format(item.prefix, len(self.data))
        self.data[key] = item

    @property
    def tcf(self):
        elem = etree.Element(P_TEXT + self.element)
        for key, child in self.data.items():
            child_elem = child.tcf
            child_elem.set('ID', key)
            elem.append(child_elem)
        return elem


class AnnotationElement:

    element = ''
    prefix = 'x'

    def __init__(self):
        self.parent = None
        self.tokens = []

    @property
    def tcf(self):
        raise NotImplementedError


class SimpleAnnotationElement(AnnotationElement):

    def __init__(self, text):
        super().__init__()
        self.text = text

    @property
    def tcf(self):
        elem = etree.Element(P_TEXT + self.element)
        elem.text = self.text
        return elem

class TextCorpus:
    """
    The main class that represents a TextCorpus.

    A TextCorpus consists of a series of AnnotationLayers.

    """

    def __init__(self, lang=None):
        self.lang = lang

    def find_token(self, token_id):
        warn('TextCorpus.find_token() is deprecated. '
             'Use TextCorpus.tokens.get() instead.')
        return self.tokens.get(token_id)


class Tokens(AnnotationLayerWithIDs):
    element = 'tokens'

    def __init__(self, initialdata=None):
        super().__init__(initialdata)
        self.pos_tagset = None

class Token(AnnotationElement):
    """
    A Token.

    """
    element = 'token'
    prefix = 't'

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.lemma = None
        self.tag = None
        self.analysis = None
        self.entity = None
        self.reference = None

    def __str__(self):
        return self.text

    @property
    def postag(self):
        """POS tag from a TagSet."""
        tagset = TagSet(self.parent.pos_tagset)
        return tagset[self.tag]

    @property
    def semantic_unit(self):
        """
        Get the semantic unit for a token.

        The semantic unit can be the lemma, a named entity, or a referenced
        semantic unit.

        """
        # TODO: Revise!
        if self.named_entity is not None:
            return self.named_entity
        elif self.reference is not None:
            return self.reference
        else:
            return self.lemma


class Sentences(AnnotationLayerWithIDs):

    element = 'sentences'


class Sentence(AnnotationElement):
    """
    Class that represents a TCF sentence.

    """
    element = 'sentence'
    prefix = 's'


class TextStructure(AnnotationLayer):

    element = 'textstructure'


class TextSpan(AnnotationElement):

    element = 'textspan'
    prefix = 'ts'

    def __init__(self):
        super().__init__()
        self.type = None


def parse(input_data, layers=None):
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(input_data, parser=parser)
    tree = etree.ElementTree(root)
    corpus_elem = tree.xpath('/data:D-Spin/text:TextCorpus',
                                namespaces=NS)[0]
    corpus = TextCorpus(lang=corpus_elem.get('lang'))
    if layers:
        layer_elems = [corpus_elem.find(P_TEXT + layer) for layer in layers]
    else:
        layer_elems = corpus_elem
    for layer_elem in layer_elems:
        tag = etree.QName(layer_elem).localname
        if tag == 'text':
            corpus.text = layer_elem.text
        elif tag == 'tokens':
            corpus.tokens = Tokens()
            for token_elem in layer_elem:
                corpus.tokens[token_elem.get('ID')] = Token(token_elem.text)
        elif tag == 'sentences':
            corpus.sentences = Sentences()
            for sentence_elem in layer_elem:
                sentence = Sentence()
                sentence.tokens = [corpus.tokens[key] for key in 
                                   sentence_elem.get('tokenIDs').split()]
                corpus.sentences[sentence_elem.get('ID')] = sentence
        elif tag == 'lemmas':
            for lemma_elem in layer_elem:
                for token_id in lemma_elem.get('tokenIDs').split():
                    corpus.tokens[token_id].lemma = lemma_elem.text
        elif tag == 'POStags':
            corpus.tokens.pos_tagset = layer_elem.get('tagset')
            for tag_elem in layer_elem:
                for token_id in tag_elem.get('tokenIDs').split():
                    corpus.tokens[token_id].tag = tag_elem.text
        elif tag == 'textstructure':
            corpus.textstructure = TextStructure()
            for span_elem in layer_elem:
                if not 'start' in span_elem.attrib:
                    # The TCF example contains textspans with no start or end
                    # attribute. The meaning of those is unclear, we skip them
                    # here.
                    continue
                span = TextSpan()
                if 'type' in span_elem.attrib:
                    span.type = span_elem.get('type')
                span.tokens = []
                start = span_elem.get('start')
                end = span_elem.get('end')
                keys = list(corpus.tokens.keys())
                for key in keys[keys.index(start):]:
                    span.tokens.append(corpus.tokens.get(key))
                    if key == end:
                        break
                corpus.textstructure.append(span)
    return corpus
