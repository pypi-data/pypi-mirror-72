#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

from typing import Type, Iterable


from ncbi_taxonomist.model import taxon


class MapQuery:

  def __init__(self, queries:Iterable):
    self.queries = set(queries)

  def map_query(self, taxon:Type[taxon.Taxon]):
    raise NotImplementedError
