#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.base.result

class NcbiTaxonomyResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request):
    super().__init__(request.eutil, request.query_id, request.db)
    self.queries = set()
    self.taxa = {}

  def size(self):
    return len(self.queries)

  def get_link_parameter(self):
    print("{}: Entrez links not supported".format(__name__))
    return None

  def isEmpty(self):
    if not self.queries:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'queries': [x for x in self.queries]}

  def add_queries(self, queries):
    self.queries |= queries

  def add_taxon(self, taxon):
    self.taxa.update({taxon.taxon_id: taxon})
