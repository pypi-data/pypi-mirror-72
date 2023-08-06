"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import sys
import json
import logging
import resource
from typing import Mapping, Type, Iterable


from ncbi_taxonomist import utils
from ncbi_taxonomist import taxa_cache
from ncbi_taxonomist.db import dbimporter
from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.map import mapper
from ncbi_taxonomist.map import mapparser
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.convert import accessiondata
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.resolve import resolver
from ncbi_taxonomist.collect import collector


class NcbiTaxonomist:

  cache = taxa_cache.TaxaCache()

  def __init__(self, dbpath:str=None, email:str=None):
    self.logger = logging.getLogger(utils.resolve_log_nspace(NcbiTaxonomist))
    self.email = email
    self.db = None
    if dbpath:
      self.db = dbmanager.TaxonomyDb(dbpath)
      self.logger.debug("{}: Succesfully".format(self.db.path))

  def cache_taxon(self, taxon:Type[taxon.Taxon]):
    NcbiTaxonomist.cache.cache_id(taxon.taxon_id)
    NcbiTaxonomist.cache.cache_names(taxon.get_names())

  def cache_taxa(self, taxa:Mapping[int,taxon.Taxon]):
    for i in taxa:
      self.cache_taxon(taxa[i])

  def map_taxa(self, taxids:Iterable[int]=None, names:Iterable[str]=None, remote:bool=False):
    """
      Map names to taxids and vice-versa. Print mappings as JSON to STDOUT.

      :param taxids: query taxids
      :param names: query names
      :param remote: query NCBI Entrez database
    """
    tm = mapper.Mapper(self.db, self.email)
    if self.db and names:
      self.logger.debug("Map:{}::names:{}::{}".format(self.db.path, len(names), names))
      nmap = tm.map_names(names, taxadb.TaxaDbConverter(taxon.Taxon()))
    if self.db and taxids:
      self.logger.debug("Map:{}::taxids:{}::{}".format(self.db.path, len(taxids), taxids))
      tmap = tm.map_taxids(taxids, taxadb.TaxaDbConverter(taxon.Taxon()))
    if remote and names:
      self.logger.debug("Map:{}::taxids:{}::{}".format("rem", len(names), names))
      tm.map_names_remote(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))
    if remote and taxids:
      self.logger.debug("Map:{}::taxids:{}::{}".format("rem", len(taxids), taxids))
      tm.map_taxids_remote(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  def map_accessions(self, accessions:Iterable[str], entrezdb:str, remote:bool=False):
    """
      Map accessions to taxids. Print mappings as JSON to STDOUT.

      :param accessions: query taxids
      :param entrezdb: accession origin Entrez database name
      :param remote: query NCBI Entrez database
    """
    tm = mapper.Mapper(self.db, self.email)
    if self.db:
      self.logger.debug("Map:{}::{}:accs:{}:({})".format(self.db.path, entrezdb,
                                                         len(accessions), accessions))
      tm.map_accessions(accessions, entrezdb)
    if remote:
      self.logger.debug("Map:{}::{}:accs:{}:({})".format("rem", entrezdb,
                                                         len(accessions), accessions))
      tm.map_accessions_remote(accessions, entrezdb,
                               accessiondata.AccessionDataConverter(accession.AccessionData()))

  def collect(self, taxids:Iterable[int]=None, names:Iterable[str]=None):
    """Collect taxa information remotely from Entrez."""
    tc = collector.Collector(self.email)
    if names:
      self.logger.debug("\tnames::{} ({})".format(len(names), names))
      tc.collect_names(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))
    if taxids:
      self.logger.debug("\ttaxids::{} ({})".format(len(taxids), taxids))
      tc.collect_taxids(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  #def import_to_db(self, out_attrib:str, taxa:bool=False, lineage:bool=False, accessions:bool=False):
  def import_to_db(self, out_attrib:str):
    """
      Import data to local taxonomy database. Attribute names can be passed to
      filter them for piped processing. Taxa, lineages and accessions require
      specific parser.

      :param out_attrib: attribute name to filter
      :param taxa: import taxa
      :param lineage: import lineage
      :param accession: import accession
    """
    dbimporter.import_stdin(self.db, out_attrib)

  def resolve(self, taxids:Iterable[int]=None, names:Iterable[str]=None, remote:bool=False):
    """
    Resolve lineages for names and taxids. If a local database is given, it
    will be checked first, followed by checking Entrez remotely if requested.
    Lineagae are printed to STDOUT as JSON array.

    :param taxids: taxids
    :param names: taxa names
    :param remote: query NCBI Entrez database
    """
    tr = resolver.Resolver(self.db, self.email)
    if self.db and names:
      self.logger.debug("resolve::{}::names::{} ({})".format(self.db, len(names), names))
      tr.resolve_names(names, taxadb.TaxaDbConverter(taxon.Taxon()))
    if self.db and taxids:
      self.logger.debug("resolve::{}::taxids::{} ({})".format(self.db, len(taxids), taxids))
      tr.resolve_taxids(taxids, taxadb.TaxaDbConverter(taxon.Taxon()))
    if remote and names:
      self.logger.debug("resolve::{}::names::{} ({})".format("rem", len(names), names))
      tr.resolve_names_remote(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))
    if remote and taxids:
      self.logger.debug("resolve::{}::taxids::{} ({})".format("rem", len(taxids), taxids))
      tr.resolve_taxids_remote(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  def resolve_accession_map(self, remote:bool=False):
    """
    Resolve lineages for accessions from STDIN. Lineagaes are printed to STDOUT
    as JSON array.

    :param remote: query NCBI Entrez database
    """
    accs = {}
    taxids = {}
    mapparser.parse_accession_map(accs, taxids)
    tr = resolver.Resolver(self.db, self.email)
    if remote:
      self.logger.debug("resolve::{}::accessions::{}".format("rem", len(accs)))
      tr.resolve_accession_mapping_remote(taxids, accs, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  def get_subtree(self, taxa_ids:list=None, names:list=None, remote:bool=False):
    pass
