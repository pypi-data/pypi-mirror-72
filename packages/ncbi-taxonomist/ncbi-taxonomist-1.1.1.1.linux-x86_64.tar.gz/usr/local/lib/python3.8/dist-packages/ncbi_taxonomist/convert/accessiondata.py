"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping, Type


from ncbi_taxonomist.model import accession
from ncbi_taxonomist.convert import converter

class AccessionDataConverter(converter.ModelConverter):

  attribute_mapper = {'taxid' : 'taxon_id'}
  accessiontypes =['caption', 'accessionversion', 'extra']

  def __init__(self, accs_datamodel:Type[accession.AccessionData]):
    super().__init__(accs_datamodel)

  def convert_to_model(self, attributes:Mapping[str,str], srcdb) -> Type[accession.AccessionData]:
    accsattrib = {'uid':attributes.pop('uid'), 'db': srcdb, 'accessions': {}}
    for i in AccessionDataConverter.attribute_mapper:
      if i in attributes:
        accsattrib[AccessionDataConverter.attribute_mapper[i]] = attributes.pop(i)
    for i in AccessionDataConverter.accessiontypes:
      accsattrib['accessions'][i] = attributes.pop(i, None)
    return self.model.new(accsattrib)

  def convert_from_model(self, model:Type[accession.AccessionData], outdict=None)->Dict[str, str]:
    attrib = model.attributes()
    attrib.update({'accessions':{'uid':model.uid}})
    return attrib
