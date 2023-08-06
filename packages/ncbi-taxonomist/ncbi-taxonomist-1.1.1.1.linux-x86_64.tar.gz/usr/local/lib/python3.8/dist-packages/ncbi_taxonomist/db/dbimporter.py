"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
import logging
from typing import Dict, Iterable, Mapping, Type


from ncbi_taxonomist.db import dbmanager


def parse_taxa(data:Mapping[str,any], taxa:Iterable, names:Iterable):
  """Parse taxa data from STDIN"""
  taxid = data.pop('taxon_id')
  taxa.append((taxid, data.pop('rank'), data.pop('parent_id')))
  if 'names' in data:
    for i in data['names']:
      names.append((taxid, i, data['names'][i]))

def filter_attribute(line, attrib:str)->Dict[str,any]:
  """Select specific attribute to print to STDOUT after import."""
  attribs = json.loads(line.strip())
  if attrib is None:
    sys.stdout.write(line)
    return attribs
  if attrib in attribs:
    sys.stdout.write(json.dumps(attribs[attrib])+'\n')
    return attribs
  logger = logging.getLogger('ncbi-taxonomist')
  logger.info("Attribute {} not found for filtering".format(attrib))
  return attribs

def commit(db:Type[dbmanager.TaxonomyDb], taxa:Iterable[tuple], names:Iterable[tuple],
           accessions:Iterable[tuple]=None, taxids:Iterable[tuple]=None):
  """Commit data into local database. Order of commits is important."""
  if taxa:
    db.add_taxa(taxa)
    db.add_names(names)
    taxa = []
    names = []
  if accessions:
    db.add_taxids(taxids)
    db.add_accessions(accessions)
    accessions = []
    taxids = []

def parse_accession(data:Mapping[str,any], accessions:Iterable, taxids:Iterable,
                    taxa:Iterable, names:Iterable):
  """Parse accessions data from STDIN"""
  taxid = data.pop('taxon_id')
  db = data.pop('db')
  accessions.append((data.pop('uid'), 'uid', db, taxid))
  for i in data['accessions']:
    accessions.append((data['accessions'][i], i, db, taxid))
  if 'lin' in data:
    for i in data.pop('lin'):
      parse_taxa(i, taxa, names)
  taxids.append((taxid,))

def import_stdin(db:Type[dbmanager.TaxonomyDb], out_attrib:str=None):
  """Parse JSON STDIN and add data to local database"""
  taxa = []
  names = []
  taxids = []
  accessions = []
  for i in sys.stdin:
    attribs = filter_attribute(i, out_attrib)
    if 'accs' in attribs:
      if not 'data' in attribs:
        sys.exit("Missing data attribute. Expected with accessions. Abort")
      parse_accession(attribs.pop('data'), accessions, taxids, taxa, names)
      if len(accessions) % 100000 == 0:
        commit(db, taxa, names, accessions, taxids)
    elif 'lin' in attribs:
      for i in attribs.pop('lin'):
        parse_taxa(i, taxa, names)
    elif 'taxon' in attribs:
      parse_taxa(attribs.pop('taxon'), taxa, names)
    else:
      parse_taxa(attribs, taxa, names)
    if len(taxa) % 100000 == 0:
      commit(db, taxa, names)
  if taxa:
    commit(db, taxa, names)
  if accessions:
    commit(db, taxa, names, accessions, taxids)
