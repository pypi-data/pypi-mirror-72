#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys


import ncbi_taxonomist.collection.basic_collection

class SubtreeCollection(ncbi_taxonomist.collection.basic_collection.BasicCollection):

  def __init__(self, root, taxa=None):
    super().__init__(taxa=taxa, category='subtree')
    self.root = root

  def get_collection(self):
    pass

  def export_collection(self):
    c = {'root' : self.taxa.pop(self.root).get_attributes(),
         'taxa' : [self.taxa[x].get_attributes() for x in self.taxa]}
    return c
