#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from lxml import etree
from tcflib import tcf
from tcflib.test import __file__ as test_directory


class TestTCF(unittest.TestCase):

    def setUp(self):
        testfile = os.path.join(os.path.dirname(test_directory),
                                'data', 'tcf04-karin-wl.xml')
        self.tree = etree.parse(testfile, parser=tcf.parser)
        self.corpus = self.tree.xpath('/data:D-Spin/text:TextCorpus',
                                      namespaces=tcf.NS)[0]

    def test_text(self):
        text_elem = self.corpus.find(tcf.P_TEXT + 'text')
        self.assertEqual(text_elem.text,
                'Karin fliegt nach New York. Sie will dort Urlaub machen.')

    def test_token_lookup(self):
        token = self.corpus.find_token('t_0')
        self.assertEqual(token.text, 'Karin')

    def test_value_list(self):
        entity = self.tree.xpath('//text:entity[@ID = "ne_1"][1]',
                                 namespaces=tcf.NS)[0]
        oldtokens = entity.get('tokenIDs')
        values = entity.get_value_list('tokenIDs')
        self.assertEqual(len(values), 2)
        self.assertIn('t_3', values)
        self.assertEqual(values[1], 't_4')
        values.append('t_5')
        self.assertEqual(entity.get('tokenIDs'), oldtokens + ' t_5')
        entity.set('tokenIDs', oldtokens)

    def test_lemma(self):
        token = self.corpus.find_token('t_1')
        lemma = token.lemma
        self.assertEqual(lemma.tag, tcf.P_TEXT + 'lemma')
        self.assertEqual(str(lemma), 'fliegen')

    def test_pos_annotation(self):
        token = self.corpus.find_token('t_0')
        pos = token.pos
        self.assertEqual(pos.tag, tcf.P_TEXT + 'tag')
        self.assertEqual(str(pos), 'NE')

    def test_pos_tag(self):
        token = self.corpus.find_token('t_0')
        tag = token.postag
        from tcflib.tagsets.base import TagBase
        self.assertIsInstance(tag, TagBase)
        self.assertEqual(tag.pid, 'http://www.isocat.org/datcat/DC-1371')

    def test_named_entity(self):
        token = self.corpus.find_token('t_3')
        ne = token.named_entity
        self.assertEqual(ne.tag, tcf.P_TEXT + 'entity')
        self.assertEqual(str(ne), '-- York')
        self.assertEqual(ne.get('class'), 'LOC')
        tokens = [token, self.corpus.find_token('t_4')]
        self.assertEqual(ne.tokens, tokens)

    def test_references(self):
        token = self.corpus.find_token('t_8')
        ref = token.reference
        self.assertEqual(ref.tag, tcf.P_TEXT + 'reference')
        self.assertEqual(str(ref), '-- York')

    def test_semantic_unit(self):
        token = self.corpus.find_token('t_0')
        self.assertEqual(token.semantic_unit.tag, tcf.P_TEXT + 'entity')
        token = self.corpus.find_token('t_1')
        self.assertEqual(token.semantic_unit.tag, tcf.P_TEXT + 'lemma')
        token = self.corpus.find_token('t_8')
        self.assertEqual(token.semantic_unit.tag, tcf.P_TEXT + 'reference')

    def test_dependency_parse(self):
        parse = self.corpus.depparsing[0]
        root = parse.root
        self.assertEqual(root, 't_1')
        dependents = parse.find_dependents(root)
        self.assertEqual(dependents, ['t_0', 't_2'])


if __name__ == '__main__':
    unittest.main()
