"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
from typing import Type


import entrezpy.base.analyzer


from ncbi_taxonomist.map.query import accessionmapquery
from ncbi_taxonomist.remote import accessionresult
from ncbi_taxonomist.convert import accessiondata

class RemoteAccessionMapper(entrezpy.base.analyzer.EutilsAnalyzer):

  def __init__(self,
               query:Type[accessionmapquery.AccessionMapQuery],
               converter:Type[accessiondata.AccessionDataConverter]):
    super().__init__()
    self.query = query
    self.converter = converter
    self.accessiontypes = ['caption', 'accessionversion', 'extra', 'uid']

  def init_result(self, response:dict, request:object) -> bool:
    if not self.result:
      self.result = accessionresult.NcbiAccessionResult(request)
      return True
    return False

  def analyze_error(self, response:dict, request:object):
    print (json.dumps({__name__:{'Response-Error':{
                                   'request-dump' : request.dump_internals(),
                                   'error' : response}}}))

  def analyze_result(self, response:dict, request:object):
    self.init_result(request, request)
    uids = response['result'].pop('uids', None)
    if uids:
      for i in uids:
        m = self.converter.convert_to_model(response['result'].pop(i), request.db)
        self.query.map_query(self.result.add_accession(m))
