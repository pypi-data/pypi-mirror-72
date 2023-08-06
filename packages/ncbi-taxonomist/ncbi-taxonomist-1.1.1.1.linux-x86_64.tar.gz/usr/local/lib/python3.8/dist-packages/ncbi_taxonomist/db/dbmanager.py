"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import logging
import sqlite3
from typing import Iterable, Dict, List, Tuple, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.map.query import mapquery
from ncbi_taxonomist.map.query import accessionmapquery
from ncbi_taxonomist.collect.query import collectquery
from ncbi_taxonomist.db.table import taxa
from ncbi_taxonomist.db.table import names
from ncbi_taxonomist.db.table import accessions
from ncbi_taxonomist.collection import subtree_collection


class TaxonomyDb:

  def __init__(self, dbpath:str):
    self.logger = logging.getLogger(utils.resolve_log_nspace(TaxonomyDb))
    self.path = dbpath
    self.logger.debug("{}: Create instance".format(self.path))
    self.connection = self.init_connection()
    self.taxa = taxa.TaxaTable(self.path).create(self.connection)
    self.names = names.NameTable(self.path).create(self.connection)
    self.accessions = accessions.AccessionTable(self.path).create(self.connection)
    self.logger.debug("{}: Database initialized")

  def init_connection(self)->sqlite3.Connection:
    self.logger.debug("{}: Connecting".format(self.path))
    connection = sqlite3.connect(self.path)
    connection.execute("PRAGMA foreign_keys=1")
    connection.row_factory = sqlite3.Row
    self.logger.debug("{}: Connected".format(self.path))
    return connection

  def close_connection(self)->None:
    self.logger.debug("{}: Closing connection".format(self.path))
    self.connection.close()

  def connect(self) -> sqlite3.Connection:
    if self.connection is None:
      return self.init_connection(self.path)
    return self.connection

  def add_taxa(self, taxa:Iterable[Tuple[int,str,int]])->None:
    self.taxa.insert(self.connection, taxa)

  def add_taxids(self, taxids:Iterable[Tuple[int,]])->None:
    self.taxa.insert_taxids(self.connection, taxids)

  def add_names(self, names:Iterable[Tuple[int,str,str]])->None:
    self.names.insert(self.connection, names)

  def add_accessions(self, accessions:Iterable[Tuple[str, str, str, int]])->None:
    self.accessions.insert(self.connection, accessions)

  def collect_name_subtree(self, start_names, converter, torank=None):
    raise NotImplementedError

  #def collect_id_subtree(self, root_ids:Iterable[int], converter) -> List:
    #"""
    #Collect subtree for given taxon ids.
    #"""
    #collections = []
    #for i in root_ids:
      #for j in self.taxa.get_subtree(self.connection, i):
        #converter.convert_to_model({'taxon_id': j['taxon_id'],
                                    #'parent_id':j['parent_id'],
                                    #'rank':j['rank'],
                                    #'name':j['name'], 'type':j['type']})
      #collections.append(subtree_collection.SubtreeCollection(i, converter.taxa))
      #converter.reset()
    #return collections

  def get_taxa_by_name(self, names:Iterable[str], converter:Type[taxadb.TaxaDbConverter],
                       query:Type[mapquery.MapQuery]=None)->Dict[str,int]:
    """
    Find taxa by name and use the converter to format into appropriate model.

    .. todo:: Test if n.name='man' OR n.name='Bacteria OR ...' is better approach
    """
    stmt = """SELECT n.name, n.type, t.taxon_id, t.rank, t.parent_id FROM taxa t
              JOIN names n on t.taxon_id=n.taxon_id WHERE n.name=?"""
    taxa = {}
    for i in names:
      for j in self.connection.cursor().execute(stmt, (i,)):
        if j['taxon_id'] not in taxa:
          taxa[j['taxon_id']] = converter.convert_to_model({'taxon_id': j['taxon_id'],
                                                            'parent_id':j['parent_id'],
                                                            'rank':j['rank']})
        taxa[j['taxon_id']].update_names({j['name']:j['type']})
        if query:
          query.map_query(taxa[j['taxon_id']])
    return taxa

  def get_taxa_by_accessions(self, accs:Iterable[str], db:str,
                             query:Type[accessionmapquery.AccessionMapQuery]=None)->List[Dict]:
    """Find taxa by name and use converter to format appropriate model."""
    stmt = """SELECT a.accession, a.db, a.type, t.taxon_id FROM taxa t JOIN
              accessions a on t.taxon_id=a.taxon_id WHERE a.accession=? AND a.db=?"""
    if not db:
      db='%'
      stmt = """SELECT a.accession, a.db, a.type, t.taxon_id FROM taxa t JOIN
                accessions a on t.taxon_id=a.taxon_id WHERE a.accession=? AND a.db LIKE ?"""
    mappings = []
    for i in accs:
      for j in self.connection.cursor().execute(stmt, (i, db)):
        mappings.append({'accs':j['accession'], 'taxid':j['taxon_id'], 'type':j['type'], 'db':j['db']})
        if query:
          query.map_local_accession(mappings[-1])
    return mappings

  def get_taxa_by_taxids(self, taxids:Iterable[int], converter:Type[taxadb.TaxaDbConverter],
                         query:Type[mapquery.MapQuery]=None)->Dict[int, taxon.Taxon]:
    """Find taxa by taxid and use converter to format appropriate model."""
    stmt = """SELECT t.taxon_id, t.rank, t.parent_id, n.name, n.type \
              FROM taxa t JOIN names n on t.taxon_id=n.taxon_id WHERE t.taxon_id=?"""
    taxa = {}
    for i in taxids:
      for j in self.connection.cursor().execute(stmt, (i,)):
        if j['taxon_id'] not in taxa:
          taxa[j['taxon_id']] = converter.convert_to_model({'taxon_id': j['taxon_id'],
                                                            'rank':j['rank'],
                                                            'parent_id':j['parent_id']})
        taxa[j['taxon_id']].update_names({j['name']:j['type']})
        if query:
          query.map_query(taxa[j['taxon_id']])
    return taxa

  def get_taxid_lineages(self, taxids:Iterable[int],
                         converter:Type[taxadb.TaxaDbConverter])->Dict[int, taxon.Taxon]:
    """
    Find linegae for given taxon id. Found taxids are cached to avoid unnecessary
    lookups.

    .. todo:: use converters own cache
    """
    found_taxa = {}
    for i in taxids:
      if i not in found_taxa:
        for j in self.taxa.get_lineage(self.connection, i, self.names.name):
          if j['taxon_id'] not in found_taxa:
            found_taxa[j['taxon_id']] = converter.convert_to_model({'taxon_id': j['taxon_id'],
                                                                    'rank':j['rank'],
                                                                    'parent_id':j['parent_id']})
          found_taxa[j['taxon_id']].update_names({j['name']:j['type']})
    return found_taxa
