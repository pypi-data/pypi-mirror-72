"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import entrezpy.conduit


class EntrezTaxonomyQuery:

  conduit = None

  @staticmethod
  def query_taxids(taxids, analyzer):
    pipe = EntrezTaxonomyQuery.conduit.new_pipeline()
    pipe.add_fetch({'db':'taxonomy', 'id':taxids, 'mode':'xml'}, analyzer=analyzer)
    EntrezTaxonomyQuery.conduit.run(pipe).get_result()

  @staticmethod
  def query_names(names, analyzer):
    pipe = EntrezTaxonomyQuery.conduit.new_pipeline()
    sid = pipe.add_search({'db':'taxonomy', 'term':' OR '.join("\"{}\"".format(x) for x in names)})
    pipe.add_fetch({'mode':'xml'}, dependency=sid, analyzer=analyzer)
    EntrezTaxonomyQuery.conduit.run(pipe).get_result()

  @staticmethod
  def query_accessions(accessions, database, analyzer):
    pipe = EntrezTaxonomyQuery.conduit.new_pipeline()
    pipe.add_summary({'db':database, 'mode':'json', 'id': accessions}, analyzer=analyzer)
    EntrezTaxonomyQuery.conduit.run(pipe).get_result()

  def __init__(self, email):
    EntrezTaxonomyQuery.conduit = entrezpy.conduit.Conduit(email)
