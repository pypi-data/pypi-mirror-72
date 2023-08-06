#-------------------------------------------------------------------------------
#  \file ncbi_alias_table.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description
#-------------------------------------------------------------------------------

from . import taxonomy_table

class AliasTable(taxonomy_table.TaxonomyTable):

  def __init__(self, database):
    super().__init__(name='alias', database=database)

  def create(self, connection):
    stmt = """CREATE TABLE IF NOT EXISTS {}
              (
                id           INTEGER PRIMARY KEY,
                taxon_id     INT,
                alias        INT,
                FOREIGN KEY (alias) REFERENCES taxa(taxon_id),
                UNIQUE(taxon_id)
              )""".format(self.name)
    connection.cursor().execute(stmt)
    return self

  def get_rows(self, connection):
    return c.connection.cursor().execute("SELECT taxon_id, alias FROM {0}".format(self.name))

  def insert(self, connection, aliasvalues):
    stmt = """INSERT OR IGNORE INTO {0} (taxon_id, alias)
                          VALUES (?,?)""".format(self.name)
    connection.cursor().executemany(stmt, aliasvalues)
    connection.commit()
