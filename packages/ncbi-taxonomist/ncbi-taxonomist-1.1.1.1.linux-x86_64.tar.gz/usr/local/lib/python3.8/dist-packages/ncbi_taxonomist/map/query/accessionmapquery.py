"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Iterable, Mapping, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.map.query import mapquery

class AccessionMapQuery(mapquery.MapQuery):

  def __init__(self, queries:Mapping[str, int]):
    self.queries = set(queries)

  def update_queries(self, accessions:Mapping[str, str]) -> str:
    for i in accessions:
      if accessions[i] in self.queries:
        self.queries.remove(accessions[i])
        return accessions[i]
    return None

  def map_query(self, accession:Type[accession.AccessionData]) -> Dict[str, dict]:
    qryaccs = self.update_queries(accession.get_accessions())
    if qryaccs:
      utils.json_stdout({'accs': qryaccs, 'data': accession.get_attributes()})

  def map_local_accession(self, accs_data:Mapping[str, str]):
    self.queries.discard(accs_data['accs'])
    utils.json_stdout(accs_data)
