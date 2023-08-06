#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys


class TaxaCache:

  taxa_ids = set()
  taxa_names = set()

  @staticmethod
  def name_in_cache(name):
    if name in TaxaCache.taxa_names:
      return True
    return False

  @staticmethod
  def id_in_cache(taxa_id):
    if taxa_id in TaxaCache.taxa_ids:
      return True
    return False

  @staticmethod
  def remove_cached_ids(ids):
    if not ids:
      return None
    return TaxaCache.remove_cached(TaxaCache.taxa_ids, ids)

  @staticmethod
  def remove_cached_names(names):
    if not names:
      return None
    return TaxaCache.remove_cached(TaxaCache.taxa_names, names)

  @staticmethod
  def remove_cached(cache, attributes):
    noncached = []
    for i in attributes:
      if i not in cache:
        noncached.append(i)
    return noncached

  @staticmethod
  def add_to_cache(cache, attribute):
    if attribute not in cache:
      cache.add(attribute)

  @staticmethod
  def cache_ids(ids):
    for i in ids:
      TaxaCache.add_to_cache(TaxaCache.taxa_ids, i)

  @staticmethod
  def cache_id(taxa_id):
    TaxaCache.add_to_cache(TaxaCache.taxa_ids, taxa_id)

  @staticmethod
  def cache_names(names):
    for i in names:
      TaxaCache.add_to_cache(TaxaCache.taxa_names, i)

  def __init__(self):
    pass
