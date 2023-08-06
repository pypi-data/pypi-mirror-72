"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Set, Type, Iterable


from ncbi_taxonomist.remote import remotequery
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.collect import remotecollector
from ncbi_taxonomist.collect.query import namecollectquery
from ncbi_taxonomist.collect.query import taxidcollectquery


class Collector:
  """Collect taxon information from Entrez server"""
  def __init__(self, email:str):
    self.email = email

  def collect_names(self, names:Iterable[str], converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    ncq = namecollectquery.NameCollectQuery(names)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_names(names, remotecollector.RemoteCollector(ncq, converter))
    return ncq.queries

  def collect_taxids(self, taxids:Iterable[int], converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    tcq = taxidcollectquery.TaxidCollectQuery(taxids)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids(taxids, remotecollector.RemoteCollector(tcq, converter))
    return tcq.queries
