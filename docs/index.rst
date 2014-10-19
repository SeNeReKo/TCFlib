.. TCFlib documentation master file, created by
   sphinx-quickstart on Thu Oct  2 17:55:43 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TCFlib’s documentation!
==================================

TCFlib implements annotation pipelines using TCF as an interchange format. A pipeline consists of independent services that can be implemented in any language, as long as they consume and/or return TCF. This follows the design principles of the `WebLicht <http://weblicht.sfs.uni-tuebingen.de/weblichtwiki/index.php/Main_Page>`_ infrastructure.

TCFlib allows to *write* services in python3, and to *call* services from python3. Remote WebLicht services and local python/TCFlib services can be mixed freely.

Annotating Texts with TCFlib
----------------------------

At the heart of the WebLicht principle is the idea of an annotation pipeline: A sequence of services, i.e. a tokenizer, a POS tagger, and a dependency parser. TCFlib allows to call services and build pipelines in three ways:

* From the command line.

  A service’s module can be run as a command line programm, setting options as commandline parameters. Data are read from stdin and written to stdout, so pipelines can be built using shell pipes::

    tcfimporter.py --language de < indata.txt \
        | tokenizer.py \
        | postagger.py \
        | depparser.py > outdata.tcf

* Programmatically from python.

  Services are regular python classes. They can be initiated using different options. They can also be chained using the pipe syntax::

    Read('indata.txt') \
        | TcfImporter(language='de') \
        | Tokenizer() \
        | PosTagger() \
        | DepParser() \
        | Write('outdata.tcf')

* As web services via a REST interface.

  Currently, this is more theory than practice. Services can currently be run as web services, but this is less tested and has not been used in production. If a service provides a publicly accessible REST interface and announces its functionality to WebLicht, it can be integrated into an annotation pipeline using the WebLicht web-based GUI.

See the :doc:`tutorial` for a real-life example.

Working with annotated texts
----------------------------

TCF is a stand-off XML format that stores annotations as independent layers. This makes separation of annotation services and their data easier, but it makes it harder to work with annotated texts. Therefore, TCFlib allows to access the information stored in the TCF format using a python API. New annotations can be directly added using the python API and are serialized to XML when needed.

Note: Currently, only a subset of TCF is supported via the python API. Additions are welcome!

See the :doc:`tcflib.tcf`.

Building Annotation Services with TCFlib
----------------------------------------

A tcf service subclasses one of :class:`ImportingWorker <tcflib.service.ImportingWorker>`, :class:`AddingWorker <tcflib.service.AddingWorker>`, or :class:`ExportingWorker <tcflib.service.ExportingWorker>`.

See the :doc:`tcflib.service`.

Tagsets in TCFlib
-----------------

TCFlib uses the MAF tagset as specified in ISOcat (`DC-1345 <http://www.isocat.org/datcat/DC-1345>`_) as its universal tagset. Other tagsets are mapped onto DC-1345. Since DC-1345 uses a tag hierarchy, this allows to e.g. check if a token is a 'noun' or one of its subtags, like 'proper noun'.

See the :doc:`tcflib.tagsets`.

Reference
---------

.. toctree::
   :maxdepth: 3

   tutorial
   tcflib


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

