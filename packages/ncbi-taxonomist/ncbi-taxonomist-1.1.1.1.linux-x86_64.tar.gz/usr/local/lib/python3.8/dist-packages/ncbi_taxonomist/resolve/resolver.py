"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Set, Type, Iterable, Mapping


from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.remote import remotequery
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.resolve import remoteresolver
from ncbi_taxonomist.resolve.query import nameresolvequery
from ncbi_taxonomist.resolve.query import taxidresolvequery
from ncbi_taxonomist.resolve.query import accessionresolvequery


class Resolver:

  def __init__(self, db:Type[dbmanager.TaxonomyDb], email:str):
    self.db = db
    self.email = email

  def resolve_names(self,
                    names:Iterable[str],
                    converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    taxids = [x for x in self.db.map_names_to_ids(names)]
    nrq = nameresolvequery.NameResolveQuery(names).resolve(taxids,
                                                           self.db.get_taxid_lineages(taxids, converter))
    return nrq.queries

  def resolve_taxids(self,
                     taxids:Iterable[int],
                     converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    trq = taxidresolvequery.TaxidResolveQuery(taxids)
    self.db.get_taxid_lineages(taxids, converter)
    trq.resolve(taxids, self.db.get_taxid_lineages(taxids, converter))
    return trq.queries

  def resolve_names_remote(self,
                           names:Iterable[str],
                           converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    nrq = nameresolvequery.NameResolveQuery(names)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_names(names, remoteresolver.RemoteResolver(nrq, converter))
    return nrq.queries

  def resolve_taxids_remote(self,
                            taxids:Iterable[int],
                            converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    trq = taxidresolvequery.TaxidResolveQuery(taxids)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids(taxids, remoteresolver.RemoteResolver(trq, converter))
    return trq.queries


  def resolve_accession_mapping_remote(self,
                                       taxids:Mapping[int, Iterable[str]],
                                       accs:Mapping[str, Type[accession.AccessionData]],
                                       converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[str]:
    arq = accessionresolvequery.AccessionResolveQuery(taxids, accs)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids([x for x in taxids], remoteresolver.RemoteResolver(arq, converter))
    #return arq.queries
