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
Samples only sentences containing a given word from a TCF file.

"""

from tcflib.tcf import (P_TEXT, AnnotationLayer, AnnotationLayerWithIDs)
from tcflib.service import Worker, run_as_cli


class WordSampler(Worker):

    __options__ = {'word': '', 'layer': 'lemma'}

    def run(self, input_data):
        self.setup(input_data)
        self.sample()
        return self.corpus

    def sample(self):
        # Step 1: Find all sentences that contain the given word.
        tokens_to_keep = []
        for sentence in self.corpus.sentences:
            keep = False
            for token in sentence.tokens:
                if getattr(token, self.options.layer) == self.options.word:
                    keep = True
                    break
            if keep:
                tokens_to_keep.extend(sentence.tokens)
        # Step 2: Remove all annotations that point to obsolete tokens
        # TODO: Implement all possible layers
        for layer_name in ('sentences', 'lemmas', 'postags',
                           'depparsing', 'namedentities'):
            try:
                layer = getattr(self.corpus, layer_name)
            except AttributeError:
                # Annotation layer not present
                continue
            else:
                # Remove old layer
                old_layer = self.corpus._tree.find(f'//{P_TEXT}{layer.element}')
                old_layer.getparent().remove(old_layer)
                # Add to `new_layers` to force re-serialization
                self.corpus.new_layers.append(layer_name)
            removable = []
            for elem in layer:
                keep = False
                try:
                    for token in elem.tokens:
                        if token in tokens_to_keep:
                            keep = True
                            continue
                except AttributeError:
                    # Layer element has no tokens attribute.
                    # TODO: Implement more complex layers like depparsing.
                    # We simply delete everything now.
                    pass
                if not keep:
                    removable.append(elem)
            if isinstance(layer, AnnotationLayer):
                # List-like interface
                for elem in removable:
                    layer.remove(elem)
            elif isinstance(layer, AnnotationLayerWithIDs):
                # Dict-like interface
                for elem in removable:
                    del layer[elem.id]
        # Step 3: Remove obsolete tokens
        removable = []
        for token in self.corpus.tokens:
            if not token in tokens_to_keep:
                removable.append(token)
        for token in removable:
            del self.corpus.tokens[token.id]
        # Remove old layer
        old_layer = self.corpus._tree.find(f'//{P_TEXT}tokens')
        old_layer.getparent().remove(old_layer)
        # Add to `new_layers` to force re-serialization
        self.corpus.new_layers.insert(0, 'tokens')  # Make sure it’s the first layer


if __name__ == '__main__':
    run_as_cli(WordSampler)    
