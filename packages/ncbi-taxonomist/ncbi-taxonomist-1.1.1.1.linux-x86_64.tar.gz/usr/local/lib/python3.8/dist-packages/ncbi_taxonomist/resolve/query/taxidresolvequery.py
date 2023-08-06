"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable


from ncbi_taxonomist import utils
from ncbi_taxonomist.resolve.query import resolvequery


class TaxidResolveQuery(resolvequery.ResolveQuery):

  def __init__(self, queries:Iterable[int]):
    super().__init__(queries)

  def get_taxid(self, taxid:[int])->int:
    if taxid in self.queries:
      self.queries.remove(taxid)
      return taxid
    return None

  def resolve(self, taxids, taxa):
    for i in taxids:
      if self.get_taxid(i):
        utils.json_stdout({'taxid':i, 'lin':TaxidResolveQuery.resolve_lineage(i, taxa)})
