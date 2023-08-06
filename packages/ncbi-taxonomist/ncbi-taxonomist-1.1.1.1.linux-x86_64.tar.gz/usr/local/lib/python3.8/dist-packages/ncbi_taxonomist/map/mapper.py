"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import json
import logging
from typing import Set, Type, Iterable

from ncbi_taxonomist import utils
from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.map import remotemapper
from ncbi_taxonomist.map import remoteaccessionmapper
from ncbi_taxonomist.map.query import taxidmapquery
from ncbi_taxonomist.map.query import namemapquery
from ncbi_taxonomist.map.query import accessionmapquery
from ncbi_taxonomist.remote import remotequery
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.convert import accessiondata

class Mapper:

  def __init__(self, db:Type[dbmanager.TaxonomyDb], email:str):
    self.logger = logging.getLogger(utils.resolve_log_nspace(Mapper))
    self.db = db
    self.email = email

  def map_names(self, names:Iterable[str],
                converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[str]:
    self.logger.debug("locally map names")
    nmq = namemapquery.NameMapQuery(names)
    self.db.get_taxa_by_name(names, converter, nmq)
    return nmq.queries

  def map_names_remote(self, names:Iterable[str],
                       converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[str]:
    self.logger.debug("remotely map names")
    nmq = namemapquery.NameMapQuery(names)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_names(names, remotemapper.RemoteMapper(nmq, converter))
    return nmq.queries

  def map_taxids(self, taxids, converter):
    self.logger.debug("locally map taxids")
    tmq = taxidmapquery.TaxidMapQuery(taxids)
    self.db.get_taxa_by_taxids(taxids, converter, tmq)
    return tmq.queries

  def map_taxids_remote(self, taxids:Iterable[int],
                        converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    self.logger.debug("remotely map taxids")
    tmq = taxidmapquery.TaxidMapQuery(taxids)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids(taxids, remotemapper.RemoteMapper(tmq, converter))
    return tmq.queries

  def map_accessions(self, accessions:Iterable[str], entrezdb:str)->Set[str]:
    self.logger.debug("locally map accessions")
    amq = accessionmapquery.AccessionMapQuery(accessions)
    self.db.get_taxa_by_accessions(accessions, entrezdb, amq)
    return amq.queries

  def map_accessions_remote(self, accessions:Iterable[str], entrezdb:str,
                            converter:Type[accessiondata.AccessionDataConverter])->Set[str]:
    self.logger.debug("remotely map accessions")
    amq = accessionmapquery.AccessionMapQuery(accessions)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_accessions(accessions, entrezdb,
                         remoteaccessionmapper.RemoteAccessionMapper(amq, converter))
    return amq.queries
