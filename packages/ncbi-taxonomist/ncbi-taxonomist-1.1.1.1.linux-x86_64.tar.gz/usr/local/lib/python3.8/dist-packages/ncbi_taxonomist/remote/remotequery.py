#-------------------------------------------------------------------------------
#\author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#\copyright 2019 The University of Sydney
#\description
#-------------------------------------------------------------------------------

import entrezpy.conduit


class RemoteTaxonomyQuery:

  conduit = None

  @staticmethod
  def query_taxids(taxids, analyzer):
    pipe = RemoteTaxonomyQuery.conduit.new_pipeline()
    pipe.add_fetch({'db':'taxonomy', 'id':taxids, 'mode':'xml'}, analyzer=analyzer)
    RemoteTaxonomyQuery.conduit.run(pipe)

  @staticmethod
  def query_names(names, analyzer):
    pipe = RemoteTaxonomyQuery.conduit.new_pipeline()
    sid = pipe.add_search({'db':'taxonomy', 'term':' OR '.join("\"{}\"".format(x) for x in names)})
    pipe.add_fetch({'mode':'xml'}, dependency=sid, analyzer=analyzer)
    RemoteTaxonomyQuery.conduit.run(pipe)

  @staticmethod
  def query_accessions(accessions, database, analyzer):
    pipe = RemoteTaxonomyQuery.conduit.new_pipeline()
    pipe.add_summary({'db':database, 'id':accessions}, analyzer=analyzer)
    return RemoteTaxonomyQuery.conduit.run(pipe).get_result()

  def __init__(self, email):
    RemoteTaxonomyQuery.conduit = entrezpy.conduit.Conduit(email)
