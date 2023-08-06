#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

from typing import Type


class ModelConverter:

  def __init__(self, model):
    self.model = model

  def convert_to_model(self, attributes):
    raise NotImplementedError

  def convert_from_model(self, model, outdict=None):
    raise NotImplementedError
