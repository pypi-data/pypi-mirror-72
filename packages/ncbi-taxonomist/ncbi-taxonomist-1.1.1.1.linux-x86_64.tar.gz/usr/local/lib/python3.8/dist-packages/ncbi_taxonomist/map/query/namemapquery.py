"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Iterable, Type

from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.map.query import mapquery


class NameMapQuery(mapquery.MapQuery):

  def __init__(self, queries:Iterable[str]):
    super().__init__(queries)

  def update_queries(self, names:Dict[str,str]) -> str:
    for i in names:
      if i in self.queries:
        self.queries.remove(i)
        return i
    return None

  def map_query(self, taxon:Type[taxon.Taxon]):
    name = self.update_queries(taxon.get_names())
    if name:
      utils.json_stdout({'name':name, 'taxon':taxon.get_attributes()})
