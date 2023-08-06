#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import sys

class LineageResolver:

  @staticmethod
  def find_taxon(taxon_id, taxamap, aliasmap):
    if taxon_id in taxamap:
      return taxamap[taxon_id]
    alias = aliasmap.get(taxon_id)
    if not alias:
      sys.exit("Problems with taxid {0}: not in taxa or alias".format(taxon_id))
    return alias

  @staticmethod
  def assemble_lineage(taxon_id, taxamap, aliasmap):
    taxon = LineageResolver.find_taxon(taxon_id, taxamap, aliasmap)
    lineage = []
    while taxon.parent_id:
      lineage.append(taxon)
      taxon = LineageResolver.find_taxon(taxon.parent_id, taxamap, aliasmap)
    lineage.append(taxon)
    return lineage

  @staticmethod
  def resolve_lineages(taxon_ids, taxamap, aliasmap=None):
    if not aliasmap:
      aliasmap = {}
    lineages = {}
    for i in taxon_ids:
      lineages[i] = LineageResolver.resolve_lineage(i, taxamap, aliasmap)
    return lineages

  @staticmethod
  def resolve_lineage(taxon_id, taxamap, aliasmap=None):
    if not aliasmap:
      aliasmap = {}
    return LineageResolver.assemble_lineage(taxon_id, taxamap, aliasmap)

  @staticmethod
  def check_resolve(lineages):
    """Check if lineage has been resolved. Assumes lineage root->lowest rank.
    The lowest rank (last element in list) is assumed to be the query

    :param dict lineages: resolved lineages (list with taxonmodel instances)
    :return bool:
    """
    for i in lineages:
      for j in lineages[i]:
        if j.rank == 'superkingdom':
          return True
      print("W: unresolved lineage: {}:{}:{}".format(i,
                                                     lineages[i].name,
                                                     lineages[i].scientific_name),
            file=sys.stderr)
      return False

  def __init__(self):
    pass
