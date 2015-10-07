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
A POS tagger / lemmatizer based on TreeTagger.

"""

import subprocess as sp
from collections import namedtuple

from tcflib.tcf import POStags, Lemmas
from tcflib.service import AddingWorker, run_as_cli

# Use like `Model('stts', '/path/to/file')`
Model = namedtuple('Model', ['tagset', 'file'])


class TreeTagger(AddingWorker):
    """
    A wrapper for TreeTagger_ that adds Part of Speech and Lemma TCF layers.

    This class does not define the location of the executable and model files.
    It should be subclassed with the appropriate settings::

        from tcflib.examples.treetagger import TreeTagger, Model

        class MyTreeTagger(TreeTagger):
            executable = '/opt/TreeTagger/bin/tree-tagger'
            models = {'de': Model(tagset='stts',
                                  file='/opt/TreeTagger/lib/german-utf8.par')}


    .. _TreeTagger: http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/

    """

    executable = None
    models = {}
    params = ['-token', '-lemma', '-sgml', '-pt-with-lemma']

    def add_annotations(self):
        # Add base layers
        model = self.models[self.corpus.lang]
        self.corpus.add_layer(POStags(model.tagset))
        self.corpus.add_layer(Lemmas())
        # tag
        tokens = [token.text for token in self.corpus.tokens]
        cmd = [self.executable] + self.params + [model.file]
        tagger = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        outs, errs = tagger.communicate('\n'.join(tokens).encode('utf-8'))
        # TODO: Check returncode
        outlines = outs.splitlines()
        assert len(outlines) == len(self.corpus.tokens)
        for token, line in zip(self.corpus.tokens, outlines):
            _, tag, lemma = line.decode('utf-8').split('\t')
            token.tag = tag
            token.lemma = lemma


if __name__ == '__main__':
    run_as_cli(TreeTagger)
