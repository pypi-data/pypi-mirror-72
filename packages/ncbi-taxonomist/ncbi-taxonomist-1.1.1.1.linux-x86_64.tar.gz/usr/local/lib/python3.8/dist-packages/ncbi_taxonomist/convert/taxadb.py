#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


from typing import Dict, Type, Mapping


from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.convert import converter

class TaxaDbConverter(converter.ModelConverter):

  def __init__(self, taxonmodel:Type[taxon.Taxon]):
    super().__init__(taxonmodel)

  def convert_to_model(self, dbentry:Mapping) -> Type[taxon.Taxon]:
    dbentry['names'] = {}
    if 'name' in dbentry:
      dbentry['names'].update({dbentry['name']:dbentry['type']})
    return self.model.new(dbentry)

  def convert_from_model(self, model:Type[taxon.Taxon]) -> Dict[str, str]:
    return model.get_attribues()
