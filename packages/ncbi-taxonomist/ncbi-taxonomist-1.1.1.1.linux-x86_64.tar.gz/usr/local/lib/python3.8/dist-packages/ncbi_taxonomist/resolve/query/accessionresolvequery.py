#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------


from typing import Type, List, Mapping, AbstractSet, Iterable


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.resolve import lineageresolver

class AccessionResolveQuery:

  @staticmethod
  def resolve_taxon(taxid:int, taxa:Mapping[int,Type[taxon.Taxon]])->List[Type[taxon.Taxon]]:
    return [x.get_attributes() for x in lineageresolver.LineageResolver.resolve_lineage(taxid, taxa)]

  def __init__(self, taxids:Mapping[int, Iterable[str]], accs:Mapping[str, Type[accession.AccessionData]]):
    self.qry_taxids = taxids
    self.accs = accs

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[taxon.Taxon]]):
    for i in taxids:
      if i in self.qry_taxids:
        lin = AccessionResolveQuery.resolve_taxon(i, taxa)
        for j in self.qry_taxids[i]:
          if j in self.accs:
            accsdata = self.accs[j].get_attributes()
            accsdata.update({'lin':lin})
            utils.json_stdout({'accs':j, 'data':accsdata})
