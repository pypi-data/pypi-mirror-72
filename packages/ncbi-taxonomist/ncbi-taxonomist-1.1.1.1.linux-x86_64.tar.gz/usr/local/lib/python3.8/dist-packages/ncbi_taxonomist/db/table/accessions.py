#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description
#-------------------------------------------------------------------------------


import sqlite3
from typing import Iterable, Tuple, Type


from ncbi_taxonomist.db.table import basetable

class AccessionTable(basetable.BaseTable):

  def __init__(self, database):
    super().__init__('accessions', database=database)

  def create(self, connection:Type[sqlite3.Connection]) -> __qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS {}
              (id        INTEGER PRIMARY KEY,
               accession TEXT NOT NULL,
               db        TEXT NOT NULL,
               type      TEXT NULL,
               taxon_id  INT NOT NULL,
               FOREIGN KEY (taxon_id) REFERENCES taxa(taxon_id),
               UNIQUE(accession, db))""".format(self.name)
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection) -> None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON {1} (accession)""".format(self.idx, self.name)
    connection.cursor().execute(stmt)

  def get_rows(self, connection) -> Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT accession, db, taxon_id FROM {0}".format(self.name))

  def insert(self, connection, values:Iterable[Tuple[str, str, str, int]]) -> None:
    stmt = """INSERT OR IGNORE INTO {0} (accession, type, db, taxon_id) VALUES (?,?,?,?)""".format(self.name)
    connection.cursor().executemany(stmt, values)
    connection.commit()
