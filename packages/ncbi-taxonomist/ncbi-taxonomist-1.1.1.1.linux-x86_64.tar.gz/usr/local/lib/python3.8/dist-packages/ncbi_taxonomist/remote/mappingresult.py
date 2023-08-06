#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.base.result

class NcbiMappingResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request):
    super().__init__(request.eutil, request.query_id, request.db)
    self.mappings = {}

  def size(self):
    return len(self.mappings)

  def get_link_parameter(self):
    print("{}: Entrez links not supported".format(__name__))
    return None

  def isEmpty(self):
    if not self.mappings:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'mapping': [x for x in self.mappings]}

  def add_mapping(self, mapping):
    self.mappings.update(mapping)
