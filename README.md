TCFlib
======

The TCFlib provides a set of convenience APIs to work with the [TCF] file format and develop new services for the [WebLicht] environment.

Note: The API is not final, yet. Feedback and patches are highly welcome!

TCFlib contains three modules: [tcflib.tcf], [tcflib.service] and [tcflib.tagsets].

tcflib.tcf
----------

This module contains a convenience API for TCF files. It is based on [lxml]. Besides the standard lxml/ElementTree API, some convenience functions are added for common TCF elements.

Below, some basic features of the API are shown, using the TCF example file.

```python
from lxml import etree
from tcflib import tcf

tree = etree.parse('karin.xml', parser=tcf.parser)
corpus = tree.xpath('/data:D-Spin/text:TextCorpus', namespaces=tcf.NS)[0]
print(corpus.find(tcf.P_TEXT + 'text').text)
```

```
Karin fliegt nach New York. Sie will dort Urlaub machen.
```

The corpus sub-elements can be accessed in a property style:

```python
corpus.tokens
```

```
<Element {http://www.dspin.de/data/textcorpus}tokens at 0x7f7859488830>
```

A `<token>` has a couple of lookup functions:

```python
token = corpus.tokens[0]
token.lemma
```

```
<Element {http://www.dspin.de/data/textcorpus}lemma at 0x7f78594888f0>
```

```python
str(token.lemma)
```

```
'Karin'
```

TCFlib also has extended support for named entities:

```python
token = self.corpus.find_token('t_3')
ne = token.named_entity
str(ne)
```

```
'-- York'
```

```python
len(ne.tokens)
```

```
2
```

For easier processing in analysis application, a `semantic_unit` property is provided. It resolves references and named entities.

```python
token = corpus.find_token('t_8')  # 'dort'
str(token.semantic_unit)
```

```
'-- York'
```

For dependency parse trees, tree traversal is supported:

```python
parse = corpus.depparsing[0]
dependents = parse.find_dependents(parse.root)
```

```
['t_0', 't_2']
```

tcflib.service
--------------

A TCF service is an application that either takes TCF input and adds an annotation layer (adding service), or converts from or to TCF format (replacing service). Usually, such services are web applications that take input via POST requests and return output. For testing purpuses, TCFlib also supports running services as command line applications locally, passing input via STDIN and getting output via STDOUT.

For this purpose, `tcflib.service` provides two base classes: `AddingWorker` and `ReplacingWorker`. Options are handled transparently, so they can be passed using either command line arguments or GET parameters.


[lxml]: http://lxml.de/
[TCF]: http://weblicht.sfs.uni-tuebingen.de/weblichtwiki/index.php/The_TCF_Format
[WebLicht]: http://weblicht.sfs.uni-tuebingen.de/weblichtwiki/index.php/Main_Page

