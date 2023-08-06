#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys
import json

class BasicCollection:

  def __init__(self, name=None, taxa=None, category=None):
    self.name = name
    self.taxa = {} if taxa is None else taxa
    self.category = category

  def size(self):
    return len(taxa)

  def add_taxa(self, taxa):
    self.taxa.update(taxa)

  def get_collection(self):
    raise NotImplementedError
