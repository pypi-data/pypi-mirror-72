"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
from typing import Dict, Mapping


from ncbi_taxonomist.model import basemodel

class AccessionData(basemodel.BaseModel):

  def __init__(self, attributes:Mapping=None):
    super().__init__()
    attributes = AccessionData.standardize_attributes(attributes)
    self.taxon_id = attributes.pop('taxon_id', None)
    self.uid = attributes.pop('uid', None)
    self.db = attributes.pop('db', None)
    self.accessions = attributes.pop('accessions', {})

  def update_accessions(self, accession:Mapping[str,str]):
    """Update accessions from dictionary with structure accession:type"""
    self.accessions.update(accession)

  def get_attributes(self) -> Dict[str,any]:
    return {'taxon_id':self.taxon_id,
            'accessions':self.accessions,
            'db':self.db,
            'uid':self.uid}

  def get_accessions(self)->Dict[str,str]:
    """Return accessions as dictionary"""
    return self.accessions
