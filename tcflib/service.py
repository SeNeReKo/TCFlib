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

import requests
from lxml import etree

from tcflib import tcf


class Worker(object):
    """
    A :class:`Worker` is responsible for running a single transformation.
    This is the base class.

    Input data are passed to a :class:`Worker` instance during
    initialization. The :class:`Worker` class implements a :meth:`run`
    method that returns the output data.

    For efficiency reasons, a worker can get either a byte string or a
    :class:`tcf.TextCorpus` as input. This allows to pass
    :class:`tcf.TextCorpus` objects around without serializing them. If a byte
    string serialization is required, use :func:`tcf.serialize`.

    """

    __options__ = {}
    layers = None

    def __init__(self, **options):
        """Initialize a Worker instance with a set of options."""
        logging.debug('Init worker {}.'.format(type(self).__name__))
        self.options = argparse.Namespace()
        vars(self.options).update(self.__options__)
        if options:
            vars(self.options).update(options)
            logging.debug('Using options: {}'.format(self.options))
        else:
            logging.debug('Using default options: {}'.format(self.options))

    def __ror__(self, input_data):
        return self.run(input_data)

    def setup(self, input_data):
        """Read input_data and parse them into a :class:`tcf.TextCorpus`."""
        if isinstance(input_data, tcf.TextCorpus):
            self.corpus = input_data
        else:
            self.corpus = tcf.TextCorpus(input_data, layers=self.layers)

    def run(self, input_data):
        """
        This method is called to perform the actual data transformation.
        Subclasses must override this method.

        """
        pass


class AddingWorker(Worker):
    """
    An :class:`AddingWorker` adds annotations to the input data.

    """

    def run(self, input_data):
        """
        Parse input data and run annotation.

        Subclasses usually do not override this method, but
        :meth:`add_annotations`.

        """
        self.setup(input_data)
        self.add_annotations()
        return self.corpus

    def add_annotations(self):
        """Subclasses usually override this method."""
        pass


class ImportingWorker(Worker):
    """
    An :class:`ImportingWorker` converts input data to TCF.

    """
    def setup(self, input_data):
        self.input_data = input_data

    def run(self, input_data):
        """
        Parse input data and run annotation.

        Subclasses usually do not override this method, but
        :meth:`import_`.

        """
        self.setup(input_data)
        return self.import_()

    def import_(self):
        """Subclasses usually override this method."""
        pass


class ExportingWorker(Worker):
    """
    A :class:`ExportingWorker` converts TCF data into other formats.

    """

    def run(self, input_data):
        """
        Parse input data and run annotation.

        Subclasses usually do not override this method, but
        :meth:`export`.

        """
        self.setup(input_data)
        return self.export()

    def export(self):
        """Subclasses usually override this method."""
        raise NotImplementedError


class RemoteWorker(Worker):
    """
    A :class:`RemoteWorker` defers the actual work to a web service.

    This class can either be instantiated directly, passing the `url`
    parameter to its constructor, or it can be subclassed, setting the `url`
    class variable.

    """

    #: The URL of the remote service.
    url = ''

    def __init__(self, **options):
        """
        :param url: The URL of the web service that should be called.

        """
        if 'url' in options:
            self.url = options['url']
            del options['url']
        super().__init__(**options)

    def run(self, input_data):
        """Pass input_data to a remote service."""
        input_data = tcf.serialize(input_data)
        response = requests.post(self.url, params=vars(self.options),
                                 data=input_data)
        return response.content


class Write(object):
    """
    A dummy worker that writes its input into a file.

    It returns the input unchanged, so it can be used to write out intermediate
    results in a chain.

    """

    def __init__(self, filename):
        self.filename = filename

    def __ror__(self, input_data):
        if input_data:
            with open(self.filename, 'wb') as outfile:
                outfile.write(tcf.serialize(input_data))
        return input_data


def Read(filename):
    """A dummy worker that reads input from a file."""
    with open(filename, 'rb') as infile:
        return infile.read()


def get_arg_parser(worker_class=None):
    """Create an ArgumentParser with default options."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--verbose', action='store_true')
    service_group = arg_parser.add_argument_group('Web service',
            'Run as web service')
    service_group.add_argument('-s', '--service', action='store_true')
    service_group.add_argument('-p', '--port', type=int, default=8080)
    cli_group = arg_parser.add_argument_group('Command line',
            'Run as command line program')
    cli_group.add_argument('-i', '--infile', default=sys.stdin.buffer,
                           type=argparse.FileType('rb'))
    cli_group.add_argument('-o', '--outfile', default=sys.stdout.buffer,
                           type=argparse.FileType('wb'))
    if worker_class:
        for key, value in worker_class.__options__.items():
            if isinstance(value, list):
                vtype = type(value[0])
                cli_group.add_argument('--' + key, default=value, type=vtype,
                                       nargs='*')
            else:
                cli_group.add_argument('--' + key, default=value,
                                       type=type(value))
    return arg_parser


def run_as_cli(worker_class):
    """
    Run a worker from the commandline.

    In order for a worker to be called from the command line, the module
    defining the worker should call :func:`run_as_cli` when run standalone.

    """
    # Parse commandline arguments
    arg_parser = get_arg_parser(worker_class)
    args = arg_parser.parse_args()
    # Find extra options that should be passed to worker
    worker_args = vars(args).copy()
    for key in list(worker_args.keys()):
        if not key in worker_class.__options__:
            del worker_args[key]
    # Set up logging
    if args.verbose:
        level = logging.DEBUG
        logging.captureWarnings(True)
    else:
        level = logging.ERROR
    logging.basicConfig(level=level)
    # Run as service or cli program
    if args.service:
        run_as_service(worker_class, port=args.port)
    else:
        # Run transformation
        input_data = args.infile.read()
        worker = worker_class(**worker_args)
        output = worker.run(input_data)
        output = tcf.serialize(output)
        if output:
            args.outfile.write(output)


def run_as_service(worker_class, port):
    """Run a worker as a web service."""
    from bottle import request, route, run

    @route('/annotate', method='POST')
    def annotate():
        logging.debug('Got HTTP request.')
        worker = worker_class(**request.query)
        output = worker.run(request.body.read())
        output = tcf.serialize(output)
        return output
    run(host='localhost', port=port)