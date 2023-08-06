# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlptriples']

package_data = \
{'': ['*']}

install_requires = \
['benepar[cpu]>=0.1.2,<0.2.0',
 'cython>=0.29.16,<0.30.0',
 'numpy>=1.18.2,<2.0.0',
 'spacy>=2.2.4,<3.0.0',
 'tensorflow==1.15.2']

setup_kwargs = {
    'name': 'nlptriples',
    'version': '0.1.4',
    'description': 'A package to extract Triples in form of [predictate , object , subject]  form text ',
    'long_description': '# NLPTriples\nExtract NLP (RDF) Triples from a sentence\n\n# Overview\nA minimalistic library to extract triples from sentences. Implemented [paper](http://ailab.ijs.si/dunja/SiKDD2007/Papers/Rusu_Trippels.pdf) \n\nConverted the [api](https://github.com/tdpetrou/RDF-Triple-API) created by [Ted Petrou](https://github.com/tdpetrou) to a simple library which can be be run directly.\n\n# Installation \nInstall using pip\n\n```pip install nlptriples```\n\n# Usage\n```python\nfrom nlptriples import triples,setup\nrdf = triples.RDF_triple()\ntriple = rdf.extract(sent)\nprint(triple)\n```\n\n# Imeplemetation\n1. Constituency Parse tree is create using Berkeley Neural Parser library. (the paper uses CoreNLP)\n2. The algorithm described in the [paper](http://ailab.ijs.si/dunja/SiKDD2007/Papers/Rusu_Trippels.pdf) is used to extract triples from parse trees.\n',
    'author': 'adityaparkhi',
    'author_email': 'theaditya140@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
