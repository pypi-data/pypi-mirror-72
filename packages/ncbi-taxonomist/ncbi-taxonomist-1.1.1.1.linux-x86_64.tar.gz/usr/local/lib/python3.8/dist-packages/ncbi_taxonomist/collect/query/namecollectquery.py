"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
from typing import Iterable, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.collect.query import collectquery


class NameCollectQuery(collectquery.CollectQuery):

  def __init__(self, queries:Iterable[str]):
    super().__init__(queries)

  def update_queries(self, taxon:Type[taxon.Taxon]):
    for i in taxon.get_names():
      if i in self.queries:
        self.queries.remove(i)

  def collect(self, taxon):
    self.update_queries(taxon)
    utils.json_stdout(taxon.get_attributes())
