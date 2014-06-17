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

By using lxml's custom element classes, the API defines convenience methods
for common TCF elements.

"""

from collections.abc import MutableSequence, MutableSet
from warnings import warn

from lxml import etree

from tcflib.tagsets import TagSet

NS_DATA = 'http://www.dspin.de/data'
P_DATA = '{' + NS_DATA + '}'
NS_TEXT = 'http://www.dspin.de/data/textcorpus'
P_TEXT = '{' + NS_TEXT + '}'
NS = {'data': NS_DATA, 'text': NS_TEXT}


class AttributeValueSet(MutableSet):

    def __init__(self, node, name, iterable=None):
        self.node = node
        self.name = name
        if iterable:
            node.set(name, ' '.join(iterable))

    def __contains__(self, elem):
        if self.name in self.node.attrib:
            return ' ' + elem + ' ' in ' ' + self.node.get(self.name) + ' '
        else:
            return False

    def __iter__(self):
        if self.name in self.node.attrib:
            return iter(self.node.get(self.name).split())
        else:
            return iter([])

    def __len__(self):
        if self.name in self.node.attrib:
            return len(self.node.get(self.name).split())
        else:
            return 0

    def add(self, elem):
        if not elem in self:
            if self.name in self.node.attrib:
                self.node.set(self.name,
                              self.node.get(self.name) + ' ' + elem)
            else:
                self.node.set(self.name, elem)

    def discard(self, elem):
        if elem in self:
            elems = self.node.get(self.name).split()
            elems.remove(elem)
            if elems:
                self.node.set(self.name, ' '.join(elems))
            else:
                del self.node.attrib[self.name]


class AttributeValueList(MutableSequence):

    def __init__(self, node, name, iterable=None):
        self.node = node
        self.name = name
        if iterable:
            node.set(name, ' '.join(iterable))

    def __contains__(self, elem):
        if self.name in self.node.attrib:
            return ' ' + elem + ' ' in ' ' + self.node.get(self.name) + ' '
        else:
            return False

    def __iter__(self):
        if self.name in self.node.attrib:
            return iter(self.node.get(self.name).split())
        else:
            return iter([])

    def __len__(self):
        if self.name in self.node.attrib:
            return len(self.node.get(self.name).split())
        else:
            return 0

    def __getitem__(self, key):
        if self.name in self.node.attrib:
            return self.node.get(self.name).split()[key]
        else:
            return [][key]  # Throw same exception as a list would

    def __setitem__(self, key, elem):
        if self.name in self.node.attrib:
            elems = self.node.get(self.name).split()
        else:
            elems = []
        elems[key] = elem
        self.node.set(self.name, ' '.join(elems))

    def __delitem__(self, key):
        if self.name in self.node.attrib:
            elems = self.node.get(self.name).split()
            del elems[key]
            if elems:
                self.node.set(self.name, ' '.join(elems))
            else:
                del self.node.attrib[self.name]
        else:
            del [][key]  # Throw same exception as a list would

    def insert(self, i, elem):
        if self.name in self.node.attrib:
            elems = self.node.get(self.name).split()
        else:
            elems = []
        elems.insert(i, elem)
        self.node.set(self.name, ' '.join(elems))


class TCFElement(etree.ElementBase):
    """
    Element base class that represents a generic TCF element.

    """
    _position_xpath = etree.XPath('count(./preceding-sibling::*)+1',
                                  namespaces=NS)
    PREFIX = 'x'

    @property
    def position(self):
        return int(self._position_xpath(self))

    def get_value_list(self, name):
        """
        Get a value list for an attribute.

        Some attributes, like tokenIDs, can carry lists of values. This method
        does not return the raw attribute value string, but an
        `AttributeValueList` proxy that provides a MutableSequence interface
        for the attribute values.
        """
        return AttributeValueList(self, name)

    def set_value_list(self, name, iterable):
        """
        Set an attribute from a list.
        """
        self.set(name, ' '.join(iterable))

    def get_value_set(self, name):
        """
        Get a value list for an attribute.

        Some attributes, like tokenIDs, can carry lists of values. This method
        does not return the raw attribute value string, but an
        `AttributeValueSet` proxy that provides a MutableSet interface for the
        attribute values.
        """
        warn('Deprecated. Use `get_value_list` instead.', DeprecationWarning)
        return AttributeValueSet(self, name)

    def set_value_set(self, name, iterable):
        """
        Set an attribute from a list.
        """
        warn('Deprecated. Use `set_value_list` instead.', DeprecationWarning)
        self.set(name, ' '.join(iterable))

    def add(self, element):
        eid = element.PREFIX + str(len(self))
        element.set('ID', eid)
        self.append(element)
        return eid


class CorpusElement(TCFElement):
    """
    Element class that represents a TCF corpus.

    """
    _token_xpath = etree.XPath('text:tokens/text:token[@ID = $id][1]',
                               namespaces=NS)

    def __getattr__(self, name):
        """
        Generic child lookup method: Children can be accessed as attributes.

        TextCorpus elements contain annotations as child elements. For
        convenience, this method allows for attribute-type lookups of
        annotation elements.

        """
        child = self.find(P_TEXT + name)
        if child is not None:
            return child
        else:
            raise AttributeError

    def find_token(self, token_id):
        tokens = self._token_xpath(self, id=token_id)
        if tokens:
            return tokens[0]
        else:
            return None


class TokenElement(TCFElement):
    """
    Element class that represents a TCF token.

    """
    _pos_tagset_xpath = etree.XPath('string(/data:D-Spin/text:TextCorpus/'
                                    'text:POStags/@tagset[1])',
                                    namespaces=NS)
    _pos_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                             'text:POStags/text:tag[contains('
                             'concat(" ", @tokenIDs, " "),'
                             'concat(" ", $id, " "))][1]',
                             namespaces=NS)
    _lemma_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                               'text:lemmas/text:lemma[contains('
                               'concat(" ", @tokenIDs, " "),'
                               'concat(" ", $id, " "))][1]',
                               namespaces=NS)
    _ne_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                            'text:namedEntities/text:entity[contains('
                            'concat(" ", @tokenIDs, " "),'
                            'concat(" ", $id, " "))][1]',
                            namespaces=NS)
    _ref_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                             'text:references/text:entity/text:reference['
                             'contains(concat(" ", @tokenIDs, " "),'
                             'concat(" ", $id, " "))][1]',
                             namespaces=NS)
    PREFIX = 't'

    @property
    def postag(self):
        """POS tag from a TagSet."""
        tagset_name = self._pos_tagset_xpath(self)
        tagset = TagSet(tagset_name)
        return tagset[str(self.pos)]

    @property
    def pos(self):
        """POS annotation."""
        result = self._pos_xpath(self, id=self.get('ID'))
        if result:
            return result[0]
        else:
            return None

    @property
    def lemma(self):
        """Lemma annotation."""
        result = self._lemma_xpath(self, id=self.get('ID'))
        if result:
            return result[0]
        else:
            return None

    @property
    def named_entity(self):
        """Entity annotation."""
        result = self._ne_xpath(self, id=self.get('ID'))
        if result:
            return result[0]
        else:
            return None

    @property
    def reference(self):
        """Reference annotation."""
        result = self._ref_xpath(self, id=self.get('ID'))
        if result:
            return result[0]
        else:
            return None

    @property
    def semantic_unit(self):
        """
        Get the semantic unit for a token.

        The semantic unit can be the lemma, a named entity, or a referenced
        semantic unit.

        """
        if self.named_entity is not None:
            return self.named_entity
        elif self.reference is not None:
            return self.reference
        else:
            return self.lemma


class AnnotationElement(TCFElement):
    """
    Element class that represents a token annotation in TCF.

    This class is a base for several annotation elements like lemma or entity.

    """
    _tokens_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                               'text:tokens/text:token[contains('
                               'concat(" ", $ids, " "),'
                               'concat(" ", @ID, " "))]',
                               namespaces=NS)

    def __str__(self):
        return self.text or ''

    @property
    def tokens(self):
        return self._tokens_xpath(self, ids=self.get('tokenIDs'))


class SentenceElement(AnnotationElement):
    """
    Element class that represents a TCF sentence.

    """
    PREFIX = 's'


class TagElement(AnnotationElement):
    """
    Element class that represents a TCF POS tag.

    """
    PREFIX = 'pt'


class LemmaElement(AnnotationElement):
    """
    Element class that represents a TCF lemma.

    """
    PREFIX = 'le'


class EntityElement(AnnotationElement):
    """
    Element class that represents a TCF namedEntity.

    """
    def __str__(self):
        return ' '.join([str(token.lemma) for token in self.tokens])


class ReferenceElement(AnnotationElement):
    """
    Element class that represents a TCF reference.

    """
    _ref_tokens_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                               'text:tokens/text:token[contains('
                               'concat(" ", //text:reference[@ID = $target]/'
                               '@tokenIDs, " "),'
                               'concat(" ", @ID, " "))]',
                               namespaces=NS)
    PREFIX = 'rc'

    def __str__(self):
        return ' '.join([str(token.lemma) for token in self.tokens])

    @property
    def tokens(self):
        if 'target' in self.attrib:
            return self._ref_tokens_xpath(self, target=self.get('target'))
        else:
            return super().tokens


class TextspanElement(TCFElement):
    """
    Element class that represents a TCF text span.
    
    """
    _token_xpath = etree.XPath('/data:D-Spin/text:TextCorpus/'
                               'text:tokens/text:token[@ID = $id][1]',
                               namespaces=NS)
    _following_token_xpath = etree.XPath('following-sibling::text:token',
                                         namespaces=NS)
    PREFIX = 'ts'

    @property
    def tokens(self):
        tokens = []
        first_token = self._token_xpath(self, id=self.get('start'))[0]
        tokens.append(first_token)
        if self.get('start') == self.get('end'):
            return tokens
        for token in self._following_token_xpath(first_token):
            tokens.append(token)
            if token.get('ID') == self.get('end'):
                break
        return tokens


class ParseElement(TCFElement):
    """
    Element class that represents a TCF dependency parse.

    """
    _root_xpath = etree.XPath('text:dependency[@func = "ROOT"][1]/@depIDs',
                              namespaces=NS)
    _dependents_xpath = etree.XPath('text:dependency[@govIDs = $head]/@depIDs',
                                    namespaces=NS)
    PREFIX = 'd'

    @property
    def root(self):
        try:
            return self._root_xpath(self)[0]
        except IndexError:
            # Got no explicit root, find out.
            deps = self.xpath('text:dependency/@depIDs', namespaces=NS)
            govs = self.xpath('text:dependency/@govIDs', namespaces=NS)
            roots = set(govs) - set(deps)
            if len(roots) != 1:
                import logging, sys
                logging.error('Could not find root for parse #{}.'.format(
                              parse.position))
                sys.exit(-1)
            for root in roots:
                return root

    def find_dependents(self, head):
        dependents = self._dependents_xpath(self, head=head)
        if not dependents:
            dependents = []
        return dependents


class GraphElement(TCFElement):
    """
    Element class that represents a TCF graph.

    This class is mainly a convenience wrapper around the nodes and edges
    container elements and duplicates their node/edge handling methods.

    """
    def find_node(self, label):
        return self.find(P_TEXT + 'nodes').find_node(label)

    def add_node(self, label):
        return self.find(P_TEXT + 'nodes').add_node(label)

    def find_edge(self, a, b, directed=False):
        return self.find(P_TEXT + 'edges').find_edge(a, b, directed=directed)

    def add_edge(self, a, b, **attribs):
        return self.find(P_TEXT + 'edges').add_edge(a, b, **attribs)


class NodesElement(TCFElement):
    """
    Element class that represents a TCF nodes container.

    """
    _node_xpath = etree.XPath('text:node[text() = $label][1]',
                              namespaces=NS)

    def find_node(self, label):
        nodes = self._node_xpath(self, label=str(label))
        if nodes:
            return nodes[0]
        return None

    def add_node(self, label):
        node = Element(P_TEXT + 'node')
        node.text = str(label)
        self.add(node)
        return node


class EdgesElement(TCFElement):
    """
    Element class that represents a TCF edges container.

    """
    _edge_xpath = etree.XPath('text:edge[@source = $a and @target = $b][1]',
                              namespaces=NS)

    def find_edge(self, a, b, directed=False):
        edges = self._edge_xpath(self, a=a, b=b)
        if not edges and not directed:
            edges = self._edge_xpath(self, a=b, b=a)
        if edges:
            return edges[0]
        else:
            return None

    def add_edge(self, a, b, **attribs):
        edge = Element(P_TEXT + 'edge', **attribs)
        edge.set('source', a)
        edge.set('target', b)
        self.add(edge)
        return edge


class NodeElement(TCFElement):
    PREFIX = 'n'


class EdgeElement(TCFElement):
    PREFIX = 'e'


# Set up lookup scheme
lookup = etree.ElementNamespaceClassLookup()
parser = etree.XMLParser(remove_blank_text=True)
parser.set_element_class_lookup(lookup)

text_namespace = lookup.get_namespace(NS_TEXT)
text_namespace[None] = TCFElement
text_namespace['TextCorpus'] = CorpusElement
text_namespace['token'] = TokenElement
text_namespace['sentence'] = SentenceElement
text_namespace['tag'] = TagElement
text_namespace['lemma'] = LemmaElement
text_namespace['entity'] = EntityElement
text_namespace['reference'] = ReferenceElement
text_namespace['textspan'] = TextspanElement
text_namespace['parse'] = ParseElement
text_namespace['graph'] = GraphElement
text_namespace['nodes'] = NodesElement
text_namespace['edges'] = EdgesElement
text_namespace['node'] = NodeElement
text_namespace['edge'] = EdgeElement

Element = parser.makeelement
SubElement = etree.SubElement
