"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
from typing import Type


import entrezpy.base.analyzer
import taxonompy.parser.xmlparser

from ncbi_taxonomist.remote import taxonomyresult
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.resolve.query import resolvequery


class RemoteResolver(entrezpy.base.analyzer.EutilsAnalyzer):

  taxa = {}

  def __init__(self, query:Type[resolvequery.ResolveQuery], converter:Type[ncbitaxon.NcbiTaxonConverter]):
    super().__init__()
    self.query = query
    self.converter = converter
    self.taxonomy_parser = taxonompy.parser.xmlparser.NcbiTaxoXmlParser(RemoteResolver.taxa)

  def init_result(self, response, request:object) -> bool:
    if not self.result:
      self.result = taxonomyresult.NcbiTaxonomyResult(request)
      return True
    return False

  def analyze_error(self, response, request:object):
    print (json.dumps({__name__:{'Response-Error':{
                                   'request-dump' : request.dump_internals(),
                                   'error' : response.getvalue()}}}))

  def analyze_result(self, response, request:object):
    self.init_result(request, request)
    results = self.taxonomy_parser.parse(response)
    self.result.add_queries(results.queries)
    for i in results.taxa:
      self.result.add_taxon(self.converter.convert_to_model(results.taxa[i].attribute_dict()))
    self.query.resolve(results.queries, self.result.taxa)
