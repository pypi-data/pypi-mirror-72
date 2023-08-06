#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

from typing import Type, Mapping, List, AbstractSet, Iterable


from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.resolve import lineageresolver


class ResolveQuery:

  @staticmethod
  def resolve_lineage(taxid:int, taxa:Mapping[int,Type[taxon.Taxon]])->List[Type[taxon.Taxon]]:
    return [x.get_attributes() for x in lineageresolver.LineageResolver.resolve_lineage(taxid, taxa)]

  def __init__(self, queries:Iterable):
    self.queries = set(queries)

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[taxon.Taxon]]):
    raise NotImplementedError
