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
import logging

from lxml import etree
try:
    import igraph
except:
    pass


from tcflib.tagsets import TagSet

NS_DATA = 'http://www.dspin.de/data'
P_DATA = '{' + NS_DATA + '}'
NS_TEXT = 'http://www.dspin.de/data/textcorpus'
P_TEXT = '{' + NS_TEXT + '}'
NS = {'data': NS_DATA, 'text': NS_TEXT}


class AnnotationLayerBase:

    element = ''

    def __init__(self, initialdata=None):
        self.corpus = None

    @property
    def tcf(self):
        elem = etree.Element(P_TEXT + self.element)
        for child in self:
            elem.append(child.tcf)
        return elem


class AnnotationLayer(AnnotationLayerBase, UserList):

    def __init__(self, initialdata=None):
        AnnotationLayerBase.__init__(self)
        UserList.__init__(self, initialdata)

class AnnotationLayerWithIDs(AnnotationLayerBase, UserDict):

    def __init__(self, initialdata=None):
        AnnotationLayerBase.__init__(self)
        self.data = OrderedDict()
        if initialdata:
            self.data.update(initialdata)

    def __iter__(self):
        return iter(self.data.values())

    def __setitem__(self, key, item):
        item.parent = self
        item.id = key
        self.data[key] = item

    def keys(self):
        return self.data.keys()

    def append(self, item):
        key = '{}_{}'.format(item.prefix, len(self.data))
        item.parent = self
        item.id = key
        self.data[key] = item


class AnnotationElement:

    element = ''
    prefix = 'x'

    def __init__(self):
        self.parent = None
        self.id = None
        self.tokens = []

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + self.element)
        if self.id is not None:
            element.set('ID', self.id)
        return element


class TextCorpus:
    """
    The main class that represents a TextCorpus.

    A TextCorpus consists of a series of AnnotationLayers.

    """

    def __init__(self, input_data=None, *, layers=None):
        self.new_layers = []
        # Parse input data.
        if not input_data:
            logging.debug('Creating new TextCorpus.')
            input_data = """
            <D-Spin xmlns="http://www.dspin.de/data" version="0.4">
              <MetaData xmlns="http://www.dspin.de/data/metadata">
                <source/>
                <Services/>
              </MetaData>
              <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="de">
              </TextCorpus>
            </D-Spin>
            """
        parser = etree.XMLParser(remove_blank_text=True)
        logging.debug('Parsing input data.')
        root = etree.fromstring(input_data, parser=parser)
        self._tree = etree.ElementTree(root)
        corpus_elem = self.tree.xpath('/data:D-Spin/text:TextCorpus',
                                      namespaces=NS)[0]
        self.lang = corpus_elem.get('lang')
        if layers:
            layer_elems = [corpus_elem.find(P_TEXT + layer) for layer in layers]
        else:
            layer_elems = corpus_elem
        for layer_elem in layer_elems:
            tag = etree.QName(layer_elem).localname
            if tag == 'text':
                logging.debug('Reading layer "{}".'.format(tag))
                self.text = Text(layer_elem.text)
            elif tag == 'tokens':
                logging.debug('Reading layer "{}".'.format(tag))
                self.tokens = Tokens()
                for token_elem in layer_elem:
                    self.tokens[token_elem.get('ID')] = Token(token_elem.text)
            elif tag == 'sentences':
                logging.debug('Reading layer "{}".'.format(tag))
                self.sentences = Sentences()
                for sentence_elem in layer_elem:
                    sentence = Sentence()
                    sentence.tokens = [self.tokens[key] for key in
                                       sentence_elem.get('tokenIDs').split()]
                    self.sentences[sentence_elem.get('ID')] = sentence
            elif tag == 'lemmas':
                logging.debug('Reading layer "{}".'.format(tag))
                for lemma_elem in layer_elem:
                    for token_id in lemma_elem.get('tokenIDs').split():
                        self.tokens[token_id].lemma = lemma_elem.text
            elif tag == 'POStags':
                logging.debug('Reading layer "{}".'.format(tag))
                self.postags = POStags(layer_elem.get('tagset'))
                for tag_elem in layer_elem:
                    for token_id in tag_elem.get('tokenIDs').split():
                        self.tokens[token_id].tag = tag_elem.text
            elif tag == 'textstructure':
                logging.debug('Reading layer "{}".'.format(tag))
                self.textstructure = TextStructure()
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
                    keys = list(self.tokens.keys())
                    for key in keys[keys.index(start):]:
                        span.tokens.append(self.tokens.get(key))
                        if key == end:
                            break
                    self.textstructure.append(span)
        # Reset new_layers
        self.new_layers = []

    def __setattr__(self, name, value):
        if isinstance(value, AnnotationLayerBase):
            self.new_layers.append(name)
            value.corpus = self
        super().__setattr__(name, value)

    @property
    def tree(self):
        corpus_elem = self._tree.xpath('/data:D-Spin/text:TextCorpus',
                                      namespaces=NS)[0]
        for layer in self.new_layers:
            corpus_elem.append(getattr(self, layer).tcf)
        self.new_layers = []
        return self._tree

    @property
    def xml(self):
        return etree.tostring(self.tree, encoding='utf8',
                              pretty_print=True, xml_declaration=True)

    def find_token(self, token_id):
        warn('TextCorpus.find_token() is deprecated. '
             'Use TextCorpus.tokens.get() instead.')
        return self.tokens.get(token_id)


class Text(AnnotationLayerBase):
    element = 'text'

    def __init__(self, text):
        self.text = text

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + 'text')
        element.text = self.text
        return element


class Tokens(AnnotationLayerWithIDs):
    element = 'tokens'


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
    def tcf(self):
        element = super().tcf
        element.text = self.text
        return element

    @property
    def postag(self):
        """POS tag from a TagSet."""
        tagset = TagSet(self.parent.corpus.postags.tagset)
        return tagset[self.tag]

    @property
    def semantic_unit(self):
        """
        Get the semantic unit for a token.

        The semantic unit can be the lemma, a named entity, or a referenced
        semantic unit.

        """
        # TODO: Add named entity and reference support
        return self.lemma or self.text


class Sentences(AnnotationLayerWithIDs):

    element = 'sentences'


class Lemmas(AnnotationLayer):

    element = 'lemmas'

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + self.element)
        for i, token in enumerate(self.corpus.tokens):
            child = etree.SubElement(element, P_TEXT + 'lemma',
                                     ID='le_{}'.format(i),
                                     tokenIDs=token.id)
            child.text = token.lemma
        return element


class POStags(AnnotationLayer):

    element = 'POStags'

    def __init__(self, tagset):
        self.tagset = tagset

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + self.element, tagset=self.tagset)
        for i, token in enumerate(self.corpus.tokens):
            child = etree.SubElement(element, P_TEXT + 'tag',
                                     ID='pt_{}'.format(i),
                                     tokenIDs=token.id)
            child.text = token.tag
        return element


class Sentence(AnnotationElement):
    """
    Class that represents a TCF sentence.

    """
    element = 'sentence'
    prefix = 's'

    @property
    def tcf(self):
        element = super().tcf
        element.set('tokenIDs', ' '.join([token.id for token in self.tokens]))
        return element


class TextStructure(AnnotationLayer):

    element = 'textstructure'


class TextSpan(AnnotationElement):

    element = 'textspan'
    prefix = 'ts'

    def __init__(self, type=None):
        super().__init__()
        self.type = type

    @property
    def tcf(self):
        element = super().tcf
        if self.tokens:
            element.set('start', self.tokens[0].id)
            element.set('end', self.tokens[-1].id)
        if self.type:
            element.set('type', self.type)
        return element

class Graph(AnnotationLayerBase):

    element = 'graph'

    def __init__(self, *, label='lemma', weight='count', type='postag'):
        try:
            self._graph = igraph.Graph()
        except NameError:
            logging.warn('The igraph package has to be installed to use the '
                         'graph annotation layer.')
            raise
        self._graph.vs['name'] = ''  # Ensure 'name' attribute is present.
        self.label = label
        self.weight = weight
        self.type = type

        class Edge:
            def __init__(self, edge, graph):
                self._edge = edge
                self._graph = graph

            def __getitem__(self, key):
                return self._edge[key]

            def __setitem__(self, key, value):
                self._edge[key] = value

            @property
            def source(self):
                return self._graph.vs[self._edge.source]

            @property
            def target(self):
                return self._graph.vs[self._edge.target]

        self._edge_cls = Edge

    @property
    def nodes(self):
        return self._graph.vs

    @property
    def edges(self):
        return [self._edge_cls(edge, self._graph) for edge in self._graph.es]

    def add_node(self, name, **attr):
        if not name in self._graph.vs['name']:
            self._graph.add_vertex(name, **attr)
        return self.node(name)

    def add_edge(self, source, target, weight=1, **attr):
        self._graph.add_edge(source, target, weight=weight, **attr)
        return self.edge(source, target)

    def node(self, name):
        if isinstance(name, igraph.Vertex):
            # It should be safe to call node() with a node as argument.
            return name
        try:
            return self._graph.vs.find(name)
        except (IndexError, ValueError):
            return None

    def edge(self, source, target):
        source = self.node(source)
        target = self.node(target)
        try:
            edge = self._graph.es.find(_within=(source.index, target.index))
            return self._edge_cls(edge, self._graph)
        except ValueError:
            return None

    def node_for_token(self, token):
        name = getattr(token, self.label)
        node = self.node(name)
        if node is None:
            node = self.add_node(name, tokenIDs=[token.id])
            if self.type == 'postag':
                node['type'] = token.postag.find_top().name
        else:
            if not token.id in node['tokenIDs']:
                node['tokenIDs'].append(token.id)
        return node

    def edge_for_tokens(self, source, target):
        names = [getattr(token, self.label)
                 for token in (source, target)]
        edge = self.edge(*names)
        if edge is None:
            edge = self.add_edge(*names, weight=1)
        else:
            edge['weight'] += 1
        return edge

    @property
    def tcf(self):
        graph = etree.Element(P_TEXT + 'graph')
        nodes = etree.SubElement(graph, P_TEXT + 'nodes')
        edges = etree.SubElement(graph, P_TEXT + 'edges')
        nid = 'n_{}'
        # simplify the graph, i.e., merge
        self._graph.simplify(combine_edges={'weight': sum,
                             'tokenIDs': lambda x: ' '.join(x)})
        for vertex in self._graph.vs:
            node = etree.SubElement(nodes, P_TEXT + 'node')
            node.text = vertex['name']
            node.set('ID', nid.format(vertex.index))
            for key, value in vertex.attributes().items():
                if key == 'name':
                    continue
                elif isinstance(value, (list, tuple)):
                    node.set(key, ' '.join(value))
                elif isinstance(value, bool):
                    node.set(key, str(value).lower())
                else:
                    node.set(key, str(value))
        for link in self._graph.es:
            edge = etree.SubElement(edges, P_TEXT + 'edge',
                                    source=nid.format(link.source),
                                    target=nid.format(link.target))
            for key, value in link.attributes().items():
                if isinstance(value, (list, tuple)):
                    edge.set(key, ' '.join(value))
                elif isinstance(value, bool):
                    edge.set(key, str(value).lower())
                else:
                    edge.set(key, str(value))
        return graph
