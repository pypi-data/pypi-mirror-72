"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
from typing import Dict, Mapping, Type


from ncbi_taxonomist.model import basemodel

class Taxon(basemodel.BaseModel):

  def __init__(self, attributes:Mapping=None):
    super().__init__()
    attributes = Taxon.standardize_attributes(attributes)
    self.taxon_id = attributes.pop('taxon_id', None)
    self.parent_id = attributes.pop('parent_id', None)
    self.rank = attributes.pop('rank', None)
    self.names = attributes.pop('names', {})
    if self.rank == 'no rank':
      self.rank = None

  def update_names(self, names:Mapping[str, str]):
    """Update taxon names from a dictionary with the structure {name:type}."""
    self.names.update(names)

  def update(self, taxon:Type[__qualname__]):
    """Update taxon names from another Taxon instance."""
    self.update_names(taxon.names)

  def get_attributes(self)->Dict[str,any]:
    """Return taxon attributes as dictionary. The scientific_name is injected to
    simplify parsing with other tools."""
    return {'taxon_id':self.taxon_id,
            'parent_id':self.parent_id,
            'rank' : self.rank,
            'name' : self.get_name_by_type(),
            'names':self.names}

  def get_names(self)->Dict[str,str]:
    """Return names as dictionary with the structure name:type"""
    return self.names

  def get_name_by_type(self, nametype:str='scientific_name')->str:
    """Return specific name type if known."""
    for i in self.names:
      if self.names[i] == nametype:
        return i
    return None
