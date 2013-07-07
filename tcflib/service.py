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
This moduls provides a base implementation of a TCF compatible web service.

"""

import sys
import argparse
import logging

from lxml import etree

from tcflib import tcf


class Worker(object):
    """
    A `Worker` is responsible for running a single transformation.

    Input data are passed to a `Worker` instance during initialization. The
    `Worker` class implements a `run` method that returns the output data.

    """

    def __init__(self, input_data):
        self.input_data = input_data

    def run(self):
        pass


class AddingWorker(Worker):
    """
    An `AddingWorker` adds annotations to the input data.

    """

    def __init__(self, input_data):
        self.tree = etree.ElementTree(etree.fromstring(input_data,
                                                       parser=tcf.parser))
        self.corpus = self.tree.xpath('/data:D-Spin/text:TextCorpus',
                                      namespaces=tcf.NS)[0]

    def run(self):
        self.add_annotations()
        return etree.tostring(self.tree, encoding='utf8', pretty_print=True)

    def add_annotations(self):
        pass


class ReplacingWorker(Worker):
    """
    A `ReplacingWorker` replaces input data by its own data. Used for importers
    and exporters.

    """
    pass


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-v', '--verbose', action='store_true')
arg_parser.add_argument('-i', '--infile', default=sys.stdin.buffer,
                        type=argparse.FileType('rb'))
arg_parser.add_argument('-o', '--outfile', default=sys.stdout.buffer,
                        type=argparse.FileType('wb'))


def run_as_cli(worker_class, arg_parser=arg_parser):
    # Parse commandline arguments
    args = arg_parser.parse_args()
    # Set up logging
    if args.verbose:
        level = logging.DEBUG
        logging.captureWarnings(True)
    else:
        level = logging.ERROR
    logging.basicConfig(level=level)
    # Run transformation
    input = args.infile.read()
    worker = worker_class(input)
    output = worker.run()
    args.outfile.write(output)
