Tutorial
========

This tutorial covers the annotation of texts using the TCFlib and `WebLicht <http://weblicht.sfs.uni-tuebingen.de/weblichtwiki/index.php/Main_Page>`_ infrastructure. [#remark]_

The idea of WebLicht is to make annotation tools available as web services. These services operate independently from each other, and exchange data in the `TCF format <http://weblicht.sfs.uni-tuebingen.de/weblichtwiki/index.php/The_TCF_Format>`_. TCFlib makes it easy to call these services from within python3.

Remote services
---------------

To call a remote service, there are two options: Subclass the :class:`RemoteWorker <tcflib.service.RemoteWorker>` class, or just use it directly with the `url` parameter.

As an example, the default plain-text-to-TCF converter can be implemented as a :class:`RemoteWorker <tcflib.service.RemoteWorker>`::

    from tcflib.service import RemoteWorker

    class ToTCFConverter(RemoteWorker):

        __options__ = {
            'informat': 'plaintext',
            'outformat': 'tcf04',
            'language': 'de'
        }
        url = 'http://weblicht.sfs.uni-tuebingen.de/rws/service-converter/convert/qp'

To convert or annotate data with any :class:`Worker <tcflib.service.Worker>`, it is first instantiated, with the possibility to override its default options. Then, the :meth:`Worker.run <tcflib.service.Worker.run>` method is called, passing the input data:

>>> from tcflib.examples.remote_tcf_converter import ToTCFConverter
>>> worker = ToTCFConverter(language='en')
>>> worker.run('This is a simple test.')
b'<?xml version="1.0" encoding="UTF-8"?>\n<D-Spin xmlns="http://www.dspin.de/data" version="0.4">\n  <MetaData xmlns="http://www.dspin.de/data/metadata">\n    <source></source>\n  </MetaData>\n  <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="en">\n    <text>This is a simple test.</text>\n  </TextCorpus>\n</D-Spin>'

Alternatively, one may use :class:`RemoteWorker <tcflib.service.RemoteWorker>` directly, passing the `url` parameter. Note that in this case, all required options must be specified explicitly:

>>> from tcflib.service import RemoteWorker
>>> worker = RemoteWorker(url='http://weblicht.sfs.uni-tuebingen.de/rws/service-converter/convert/qp',
...                       informat='plaintext', outformat='tcf04',
...                       language='en')
>>> worker.run('This is another simple test.')
b'<?xml version="1.0" encoding="UTF-8"?>\n<D-Spin xmlns="http://www.dspin.de/data" version="0.4">\n  <MetaData xmlns="http://www.dspin.de/data/metadata">\n    <source></source>\n  </MetaData>\n  <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="en">\n    <text>This is another simple test.</text>\n  </TextCorpus>\n</D-Spin>'

Local services
--------------

In some cases, the available services do not match the requirements. TCFlib makes it possible to write services in Python. These can be freely mixed with remote services. For an example of a simple python service, see `nltk_tokenizer.py` in the `examples` directory.

Building pipelines
------------------

Services can be chained using a pipe syntax. The :meth:`Worker.run <tcflib.service.Worker.run>` method is called implicitly. For convenience, :class:`Read <tcflib.service.Read>` and :class:`Write <tcflib.service.Write>` pseudo-Workers are provided that handle reading and writing data from local files.

A complete pipeline that does POS tagging, lemmatisation, and exports files in the `mallet <http://mallet.cs.umass.edu/>`_ format for topic modelling looks like this::

    from tcflib.service import RemoteWorker, Read, Write
    from tcflib.examples.nltk_tokenizer import NltkTokenizer
    from tcflib.examples.remote_tcf_converter import ToTCFConverter
    from tcflib.examples.mallet_exporter import MalletExporter

    infile = 'input.txt'
    prefix = os.path.basename(infile)
    Read(infile) \
        | ToTCFConverter(language='fr') \
        | NltkTokenizer() \
        | RemoteWorker(url='http://clarin05.ims.uni-stuttgart.de/treetagger') \
        | MalletExporter(prefix=prefix) \
        | Write(infile + '_mallet')

.. rubric:: Footnotes

.. [#remark] A first version of this tutorial was published as a `blog post <http://senereko.hypotheses.org/11>`_ on `Gods, Graves and Graphs <http://senereko.hypotheses.org/>`_.