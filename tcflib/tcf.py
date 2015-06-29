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
from itertools import chain, product
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
    """Base class for annotation layers."""

    element = ''

    def __init__(self, initialdata=None):
        #: The corpus this layer belongs to.
        self.corpus = None
        #: The parent layer, in case of nested layers.
        self.parent = None

    @property
    def tcf(self):
        """Return the layer as an `etree.Element`."""
        elem = etree.Element(P_TEXT + self.element, nsmap={None: NS_TEXT})
        for child in self:
            elem.append(child.tcf)
        return elem

    def append(self, item):
        item.parent = self
        if hasattr(item, 'corpus'):
            # Item is an AnnotationLayer itself
            item.corpus = self.corpus


class AnnotationLayer(AnnotationLayerBase, UserList):
    """Annotation layer that acts like a list of Annotations."""

    def __init__(self, initialdata=None):
        AnnotationLayerBase.__init__(self)
        UserList.__init__(self, initialdata)

    def append(self, item):
        AnnotationLayerBase.append(self, item)
        self.data.append(item)


class AnnotationLayerWithIDs(AnnotationLayerBase, UserDict):
    """Annotation layer that holds IDs of annotations.

    This class acts like a hybrid of a list and a dict: It can be used like a
    list, e.g. it has an `append` method and it iterates over its values. But
    its items can also be set and retrieved using annotation IDs with dict-
    like element access.

    """

    def __init__(self, initialdata=None):
        AnnotationLayerBase.__init__(self)
        self.data = OrderedDict()
        if initialdata:
            self.data.update(initialdata)

    def __iter__(self):
        return iter(self.data.values())

    def __setitem__(self, key, item):
        AnnotationLayerBase.append(self, item)
        if key is None:
            # When reading a file that has no IDs set,
            # behave like appending an element.
            # FIXME: This alters the input structure,
            # as it inserts previously absent IDs.
            self.append(item)
        else:
            item.id = key
            self.data[key] = item

    def keys(self):
        return self.data.keys()

    def append(self, item, n=None):
        AnnotationLayerBase.append(self, item)
        if not item.id:
            if n is None:
                n = len(self.data)
            key = '{}_{}'.format(item.prefix, n)
            item.id = key
        self.data[item.id] = item


class AnnotationElement:
    """Base class for annotation elements."""

    element = ''
    prefix = 'x'

    def __init__(self, *, tokens=None):
        #: The annotation layer the element belongs to.
        self.parent = None
        self.id = None
        self.tokens = tokens or []

    @property
    def tcf(self):
        """Return the element as an `etree.Element`."""
        element = etree.Element(P_TEXT + self.element)
        if self.id is not None:
            element.set('ID', self.id)
        if self.tokens:
            element.set('tokenIDs',
                        ' '.join([token.id for token in self.tokens]))
        return element


class TokenList(UserList):
    """Proxy token list that sets token attributes.

    Used for token lists of `AnnotationElement`s that maintain a relation
    between the element and the token. E.g., appending a token to
    `reference.tokens` should set the token’s `reference` attribute.
    """

    token_attrib = None
    annotation_elem = None

    def __init__(self, initialdata=None):
        super().__init__(initialdata)
        if initialdata:
            for token in initialdata:
                setattr(token, self.token_attrib, self.annotation_elem)

    def append(self, token):
        super().append(token)
        setattr(token, self.token_attrib, self.annotation_elem)


class TextCorpus:
    """
    The main class that represents a TextCorpus.

    A TextCorpus consists of a series of AnnotationLayers.

    :param input_data: The XML input.
    :type input_data: str or None
    :param layers: A list of layers that should be parsed.
    :type layers: list or None

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
              <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="de"/>
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
                self.add_layer(Text(layer_elem.text))
            elif tag == 'tokens':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(Tokens())
                for token_elem in layer_elem:
                    self.tokens[token_elem.get('ID')] = Token(token_elem.text)
            elif tag == 'sentences':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(Sentences())
                for sentence_elem in layer_elem:
                    sentence = Sentence()
                    sentence.tokens = [self.tokens[key] for key in
                                       sentence_elem.get('tokenIDs').split()]
                    self.sentences[sentence_elem.get('ID')] = sentence
            elif tag == 'lemmas':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(Lemmas())
                for lemma_elem in layer_elem:
                    for token_id in lemma_elem.get('tokenIDs').split():
                        self.tokens[token_id].lemma = lemma_elem.text
            elif tag == 'POStags':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(POStags(layer_elem.get('tagset')))
                for tag_elem in layer_elem:
                    for token_id in tag_elem.get('tokenIDs').split():
                        self.tokens[token_id].tag = tag_elem.text
            elif tag == 'depparsing':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(DepParsing(
                        tagset=layer_elem.get('tagset'),
                        emptytoks=layer_elem.get('emptytoks') == 'true',
                        multigovs=layer_elem.get('multigovs') == 'true'))
                for parse_elem in layer_elem:
                    parse = DepParse()
                    for dep_elem in parse_elem:
                        func = dep_elem.get('func')
                        if 'govIDs' in dep_elem.attrib:
                            gov_tokens = [self.tokens[token_id]
                                          for token_id
                                          in dep_elem.get('govIDs').split()]
                        else:
                            gov_tokens = None
                        if 'depIDs' in dep_elem.attrib:
                            dep_tokens = [self.tokens[token_id]
                                          for token_id
                                          in dep_elem.get('depIDs').split()]
                        else:
                            dep_tokens = None
                        parse.append(Dependency(func=func,
                                                gov_tokens=gov_tokens,
                                                dep_tokens=dep_tokens))
                    self.depparsing.append(parse)
            elif tag == 'namedEntities':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(NamedEntities(layer_elem.get('type')))
                for entity_elem in layer_elem:
                    entity = NamedEntity(class_=entity_elem.get('class'))
                    entity.tokens = [self.tokens[tid]
                                     for tid
                                     in entity_elem.get('tokenIDs').split()]
                    self.namedentities.append(entity)
            elif tag == 'references':
                logging.debug('Reading layer "{}".'.format(tag))
                self.references = References(
                        typetagset=layer_elem.get('typetagset'),
                        reltagset=layer_elem.get('reltagset'),
                        extrefs=layer_elem.get('extrefs'))
                for entity_elem in layer_elem:
                    entity = Entity()
                    # Collect references, as referenced References may not
                    # exists yet.
                    targets = {}
                    extref_elem = entity_elem.find(P_TEXT + 'extref')
                    if extref_elem is not None:
                        entity.extref = extref_elem.get('refid')
                    for ref_elem in entity_elem.findall(P_TEXT + 'reference'):
                        reference = Reference()
                        reference.id = ref_elem.get('ID')
                        for token_id in ref_elem.get('tokenIDs').split():
                            token = self.tokens[token_id]
                            reference.tokens.append(token)
                        if 'target' in ref_elem.attrib:
                            targets[reference.id] = ref_elem.get('target')
                        entity.append(reference)
                    for source, target in targets.items():
                        entity[source].target = entity[target]
                    self.references.append(entity)
            elif tag == 'textstructure':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(TextStructure())
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
            elif tag == 'wsd':
                logging.debug('Reading layer "{}".'.format(tag))
                self.add_layer(Wsd(layer_elem.get('src')))
                for ws_elem in layer_elem:
                    for token_id in ws_elem.get('tokenIDs').split():
                        senses = ws_elem.get('lexunits').split()
                        self.tokens[token_id].wordsenses = senses
        # Reset new_layers
        self.new_layers = []

    @property
    def tree(self):
        """
        Return the corpus as an `etree.ElementTree`.

        The original XML tree is kept in memory, so that only newly added
        layers get serialized. This makes sure that the original tree is not
        touched.

        """
        corpus_elem = self._tree.xpath('/data:D-Spin/text:TextCorpus',
                                      namespaces=NS)[0]
        for layer in self.new_layers:
            corpus_elem.append(getattr(self, layer).tcf)
        self.new_layers = []
        return self._tree

    def write(self, file_or_path, *, encoding='utf-8', pretty_print=True):
        """
        Write the XML tree into a file.

        This method writes each layer successively and discards it afterwards.
        This is more memory efficient than building the whole tree at once.

        :param file_or_path: The target to which to write the XML tree.
        :type file_or_path: A file object or a file path.

        """
        with etree.xmlfile(file_or_path, encoding=encoding) as xf:
            with xf.element(P_DATA + 'D-Spin', nsmap={None: NS_DATA}):
                # TODO: Write MetaData.
                with xf.element(P_TEXT + 'TextCorpus', lang=self.lang,
                                nsmap={None: NS_TEXT}):
                    corpus_elem = self._tree.xpath('/data:D-Spin/text:TextCorpus',
                                                  namespaces=NS)[0]
                    # Write layers from the input tree.
                    for layer_elem in corpus_elem:
                        xf.write(layer_elem, pretty_print=pretty_print)
                        layer_elem = None
                    # Write newly added layers.
                    for layer in self.new_layers:
                        layer_elem = getattr(self, layer).tcf
                        xf.write(layer_elem, pretty_print=pretty_print)
                        layer_elem = None

    def add_layer(self, layer):
        """Add an :class:`AnnotationLayerBase` object to the corpus."""
        name = type(layer).__name__.lower()
        setattr(self, name, layer)
        layer.corpus = self
        self.new_layers.append(name)


class Text(AnnotationLayerBase):
    """
    The text annotation layer.

    """
    element = 'text'

    def __init__(self, text):
        #: The unannotated text.
        self.text = text

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + 'text', nsmap={None: NS_TEXT})
        element.text = self.text
        return element


class Tokens(AnnotationLayerWithIDs):
    """
    The tokens annotation layer.

    It holds a sequence of :class:`Token` objects.

    """
    element = 'tokens'


class Token(AnnotationElement):
    """The token annotation element."""
    element = 'token'
    prefix = 't'

    def __init__(self, text):
        super().__init__()
        #: The token text.
        self.text = text
        #: The token lemma.
        self.lemma = None
        #: The POS tag value.
        self.tag = None
        self.analysis = None
        #: The :class:`NamedEntity` object for the token.
        self.entity = None
        #: The :class:`Reference` object for the token.
        self.reference = None
        #: The list of word senses for the token.
        self.wordsenses = []

    def __str__(self):
        return self.text

    @property
    def tcf(self):
        element = super().tcf
        element.text = self.text
        return element

    @property
    def postag(self):
        """The POS tag as a
        :class:`POSTagBase <tcflib.tagsets.base.POSTagBase>`"""
        tagset = TagSet(self.parent.corpus.postags.tagset)
        return tagset[self.tag]

    @property
    def semantic_unit(self):
        """
        The semantic unit for a token.

        The semantic unit can be the (disambiguated) lemma, a named entity,
        or a referenced semantic unit.

        """
        def disambiguate(token):
            if token.wordsenses:
                return '{} ({})'.format(token.lemma or token.text,
                                        ', '.join(token.wordsenses))
            return token.lemma or token.text
        tokens = None
        if self.reference:
            if self.reference.entity.extref:
                return self.reference.entity.extref
            if self.reference.target:
                tokens = self.reference.target.tokens
        elif self.entity:
            tokens = self.entity.tokens
        if tokens:
            return ' '.join([disambiguate(token) for token in tokens])
        return disambiguate(self)


class Lemmas(AnnotationLayer):
    """
    The lemmas annotation layer.

    """

    element = 'lemmas'

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + self.element, nsmap={None: NS_TEXT})
        for i, token in enumerate(self.corpus.tokens):
            child = etree.SubElement(element, P_TEXT + 'lemma',
                                     ID='le_{}'.format(i),
                                     tokenIDs=token.id)
            child.text = token.lemma
        return element


class Wsd(AnnotationLayer):
    """
    The word senses (wsd) annotation layer.

    """

    element = 'wsd'

    def __init__(self, source):
        self.source = source

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + self.element, src=self.source,
                                nsmap={None: NS_TEXT})
        for token in self.corpus.tokens:
            if token.wordsenses:
                child = etree.SubElement(element, P_TEXT + 'ws',
                                         tokenIDs=token.id,
                                         lexunits=' '.join(token.wordsenses))
        return element


class POStags(AnnotationLayer):
    """
    The POStags annotation layer.

    """

    element = 'POStags'

    def __init__(self, tagset):
        self.tagset = tagset

    @property
    def tcf(self):
        element = etree.Element(P_TEXT + self.element, tagset=self.tagset,
                                nsmap={None: NS_TEXT})
        for i, token in enumerate(self.corpus.tokens):
            child = etree.SubElement(element, P_TEXT + 'tag',
                                     ID='pt_{}'.format(i),
                                     tokenIDs=token.id)
            child.text = token.tag
        return element


class DepParsing(AnnotationLayerWithIDs):
    """
    The depparsing annotation layer.

    It holds a sequence of :class:`DepParse` objects.

    """

    element = 'depparsing'

    def __init__(self, tagset, emptytoks=False, multigovs=False):
        super().__init__()
        self.tagset = tagset
        self.emptytoks = emptytoks
        self.multigovs = multigovs
        
    @property
    def tcf(self):
        element = super().tcf
        element.set('tagset', self.tagset)
        element.set('emptytoks', str(self.emptytoks).lower())
        element.set('multigovs', str(self.multigovs).lower())
        return element


class DepParse(AnnotationLayer):
    """
    The parse annotation element.

    It holds a sequence of :class:`Dependency` objects.

    """
    
    element = 'parse'
    prefix = 'd'

    def __init__(self):
        super().__init__()
        self.id = None
        try:
            self._graph = igraph.Graph(directed=True)
            self._graph.vs['name'] = ''  # Ensure 'name' attribute is present.
        except NameError:
            logging.warn('The igraph package has to be installed to use the '
                         'tree interface to the dependency annotation layer.')
            self._graph = None

    @property
    def root(self):
        if self._graph is not None:
            root_node = self._graph.vs.find(_indegree=0)
            return self.corpus.tokens[root_node['name']]
        else:
            for dependency in self:
                if dependency.dep_tokens and not dependency.gov_tokens:
                    return dependency.dep_tokens[0]

    def append(self, item):
        super().append(item)
        if self._graph is not None:
            for gov, dep in product(item.gov_tokens, item.dep_tokens):
                for name in (gov.id, dep.id):
                    if not name in self._graph.vs['name']:
                        self._graph.add_vertex(name)
                self._graph.add_edge(gov.id, dep.id)

    def find_dependents(self, token):
        node = self._graph.vs.find(token.id)
        dep_nodes = node.neighbors(mode=igraph.OUT)
        return [self.corpus.tokens[n['name']] for n in dep_nodes]


class Dependency(AnnotationElement):
        """
        The dependecy annotation element.

        """

        element = 'dependecy'

        def __init__(self, func, gov_tokens=None, dep_tokens=None):
            super().__init__()
            self.func = func
            self.gov_tokens = gov_tokens or []
            self.dep_tokens = dep_tokens or []

        @property
        def tcf(self):
            element = super().tcf
            element.set('func', self.func)
            for attrib, tokens in (('govIDs', self.gov_tokens),
                                   ('depIDs', self.dep_tokens)):
                if tokens:
                    element.set(attrib, ' '.join([token.id for token
                                                  in self.gov_tokens]))


class NamedEntities(AnnotationLayerWithIDs):
    """
    The namedEntities annotation layer.

    It holds a sequence of :class:`NamedEntity` objects.

    """

    element = 'namedEntities'

    def __init__(self, type):
        super().__init__()
        self.type = type

    @property
    def tcf(self):
        element = super().tcf
        element.set('type', self.type)
        return element


class NamedEntity(AnnotationElement):
    """
    The token annotation element.

    """

    element = 'entity'
    prefix = 'ne'

    def __init__(self, class_=None, tokens=None):

        class _TokenList(TokenList):
            token_attrib = 'entity'
            annotation_elem = self
        self._tokens_cls = _TokenList

        self.parent = None
        self.id = None
        self.class_ = class_
        self._tokens = self._tokens_cls(tokens)

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        # This makes sure tokens contain a link to the entity.
        self._tokens = self._tokens_cls(tokens)

    @property
    def tcf(self):
        element = super().tcf
        if self.class_ is not None:
            element.set('class', self.class_)
        return element


class References(AnnotationLayer):
    """
    The references annotation layer.

    """

    element = 'references'

    def __init__(self, typetagset, reltagset, extrefs):
        super().__init__()
        self.typetagset = typetagset
        self.reltagset = reltagset
        self.extrefs = extrefs

    @property
    def tcf(self):
        element = super().tcf
        for key in ('typetagset', 'reltagset', 'extrefs'):
            value = getattr(self, key)
            if value is not None:
                element.set(key, value)
        return element


class Entity(AnnotationLayerWithIDs):
    """
    The entity annotation element.

    This class represents a coreference entity inside the references
    annotation layer. The entity inside the namedEntities annotation layer
    is represented by the :class:`NamedEntity` class. In TCF, both share
    the entity tag name.

    An entity holds a sequence of :class:`Reference` objects.

    """

    element = 'entity'

    def __init__(self):
        super().__init__()
        self.extref = None

    @property
    def tcf(self):
        element = super().tcf
        if self.extref is not None:
            er_elem = etree.Element('extref', refid=self.extref)
            element.insert(0, er_elem)
        return element

    def append(self, item):
        if item.id is not None:
            n = None
        else:
            n = sum([len(e.data) for e in self.parent])
        super().append(item, n)


class Reference(AnnotationElement):
    """
    The reference annotation element.

    """

    element = 'reference'
    prefix = 'rc'

    def __init__(self, *, type=None, rel=None, target=None, tokens=None):

        class _TokenList(TokenList):
            token_attrib = 'reference'
            annotation_elem = self
        self._tokens_cls = _TokenList

        super().__init__()
        self.type = type
        self.rel = rel
        #: The target :class:`Reference`.
        self.target = target
        self._tokens = self._tokens_cls(tokens)

    @property
    def tokens(self):
        """The tokens for this reference."""
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        # This makes sure tokens contain a link to the entity.
        self._tokens = self._tokens_cls(tokens)

    @property
    def entity(self):
        """The :class:`Entity` this reference belongs to."""
        return self.parent

    @property
    def tcf(self):
        element = super().tcf
        for key in ('type', 'rel'):
            value = getattr(self, key)
            if value is not None:
                element.set(key, value)
        if self.target is not None:
            element.set('target', self.target.id)
        return element


class Sentences(AnnotationLayerWithIDs):
    """
    The sentences annotation layer.

    It holds a sequence of :class:`Sentence` objects.

    """

    element = 'sentences'


class Sentence(AnnotationElement):
    """
    The token annotation element.

    """

    element = 'sentence'
    prefix = 's'


class TextStructure(AnnotationLayer):
    """
    The textstructure annotation layer.

    It holds a sequence of :class:`TextSpan` objects.

    """

    element = 'textstructure'


class TextSpan(AnnotationElement):
    """
    The token annotation element.

    """

    element = 'textspan'
    prefix = 'ts'

    def __init__(self, type=None):
        super().__init__()
        #: The type of span.
        self.type = type

    @property
    def tcf(self):
        element = super().tcf
        if 'tokenIDs' in element.attrib:
            # Tokens are handled in a different way here.
            del element.attrib['tokenIDs']
        if self.tokens:
            element.set('start', self.tokens[0].id)
            element.set('end', self.tokens[-1].id)
        if self.type:
            element.set('type', self.type)
        return element


class Graph(AnnotationLayerBase):
    """
    The graph annotation layer.

    This layer implements a graph API to store graph representations of the
    text (e.g., cooccurrence graphs).

    """

    element = 'graph'

    def __init__(self, *, label='lemma', weight='count'):
        try:
            self._graph = igraph.Graph()
        except NameError:
            logging.warn('The igraph package has to be installed to use the '
                         'graph annotation layer.')
            raise
        self._graph.vs['name'] = ''  # Ensure 'name' attribute is present.
        self.label = label
        self.weight = weight

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
            node = self.add_node(name, tokens=[token])
            if token.postag is not None:
                node['type'] = token.postag.name
            if token.entity:
                    node['class'] = token.entity.class_ or ''
        else:
            if not token in node['tokens']:
                node['tokens'].append(token)
        return node

    def edge_for_tokens(self, source, target, loops=False, unique=False):
        source_name, target_name = [getattr(token, self.label)
                                    for token in (source, target)]
        if not loops and source_name == target_name:
            raise LoopError
        edge = self.edge(source_name, target_name)
        edge_tokens = frozenset((source, target))
        if edge is None:
            edge = self.add_edge(source_name, target_name,
                                 weight=1,
                                 tokens=OrderedDict({edge_tokens: 1}))
        else:
            if edge_tokens in edge['tokens'].keys():
                if not unique:
                    edge['weight'] += 1
                    edge['tokens'][edge_tokens] += 1
            else:
                edge['weight'] += 1
                edge['tokens'][edge_tokens] = 1
        return edge

    @property
    def tcf(self):
        graph = etree.Element(P_TEXT + 'graph', nsmap={None: NS_TEXT})
        nodes = etree.SubElement(graph, P_TEXT + 'nodes')
        edges = etree.SubElement(graph, P_TEXT + 'edges')
        nid = 'n_{}'
        # The graph should not have multiple edges.
        if self._graph.has_multiple():
            logging.warn('Multiple edges detected. This cannot be handled '
                         'by some graph analysis applications.')
        # simplify the graph, i.e., merge
        #self._graph.simplify(combine_edges={'weight': sum,
        #                     'tokens': lambda x: list(chain.from_iterable(x))})
        for vertex in self._graph.vs:
            node = etree.SubElement(nodes, P_TEXT + 'node')
            node.text = vertex['name']
            node.set('ID', nid.format(vertex.index))
            for key, value in vertex.attributes().items():
                if key == 'name':
                    continue
                elif key == 'tokens':
                    node.set('tokenIDs',
                             ' '.join([token.id for token in value]))
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
                if key == 'tokens':
                    for (a, b), weight in value.items():
                        etree.SubElement(edge, P_TEXT + 'tokenEdge',
                                         source=str(a.id), target=str(b.id),
                                         weight=str(weight))
                elif isinstance(value, (list, tuple)):
                    edge.set(key, ' '.join(value))
                elif isinstance(value, bool):
                    edge.set(key, str(value).lower())
                else:
                    edge.set(key, str(value))
        return graph


class LoopError(Exception):
    """This exception is raised if a request to add an edge would result in a loop."""
    def __str__(self):
        return 'Trying to add a loop to the graph.'


def serialize(obj):
    """
    Serialize an object into a byte string.

    :param obj: A :class:`TextCorpus`, `etree.ElementTree` or `string`.
    :rtype: bytes

    """
    if isinstance(obj, TextCorpus):
        obj = obj.tree
    if hasattr(obj, 'xpath'):
        return etree.tostring(obj, encoding='utf8',
                              pretty_print=True, xml_declaration=True)
    try:
        # Duck-type string
        return obj.encode('utf8')
    except AttributeError:
        return obj
