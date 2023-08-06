"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Mapping, Type

import json

class BaseModel:
  """Base class for data models."""

  @classmethod
  def new(cls, attributes:Mapping=None)->__qualname__:
    """Return new instance with given attributes"""
    return cls(attributes)

  @classmethod
  def new_from_json(cls, json_attributes)->__qualname__:
    """Return new instance with attributes encoded in JSON """
    return cls.new(json.loads(json_attributes))

  @staticmethod
  def standardize_attributes(attributes:Mapping[str,any]):
    """
    Convert None into empty dictionary. See Important warning at
    https://docs.python.org/3/tutorial/controlflow.html#default-argument-values
    """
    if attributes is None:
      attributes = {}
    return attributes

  def __init__(self, attributes:Mapping=None):
    """Ctor. Set attributes as required."""
    pass

  def get_attributes(self)->Dict[str,any]:
    """Return taxon attributes as dictionary."""
    raise NotImplementedError
