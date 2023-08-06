#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import typing

import entrezpy.base.result

class NcbiAccessionResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request:object):
    super().__init__(request.eutil, request.query_id, request.db)
    self.accessions = {}

  def size(self):
    return len(self.accessions)

  def get_link_parameter(self):
    print("{}: Entrez links not supported".format(__name__))
    return None

  def isEmpty(self):
    if not self.accessions:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'accs': [x for x in self.accessions]}

  def add_accession(self, accs):
    self.accessions.update({accs.uid:accs})
    return accs
