"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable


from ncbi_taxonomist import utils
from ncbi_taxonomist.collect.query import collectquery


class TaxidCollectQuery(collectquery.CollectQuery):

  def __init__(self, queries:Iterable[int]):
    super().__init__(queries)

  def collect(self, taxon):
    self.queries.discard(taxon.taxon_id)
    utils.json_stdout(taxon.get_attributes())
