#-----------------------------------------------------------------------------
# Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
# Copyright: 2018, 2019,2020 The University of Sydney
#-----------------------------------------------------------------------------


import sqlite3
from typing import Iterable, Tuple, Type

from ncbi_taxonomist.db.table import basetable

class TaxaTable(basetable.BaseTable):

  def __init__(self, database:str):
    super().__init__(name='taxa', database=database)

  def create(self, connection:Type[sqlite3.Connection]) -> __qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS {0}
              (id           INTEGER PRIMARY KEY,
               taxon_id     INT NOT NULL,
               rank         TEXT NULL,
               parent_id    INT NULL,
               UNIQUE(taxon_id))""".format(self.name)
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON {1} (taxon_id)""".format(self.idx, self.name)
    connection.cursor().execute(stmt)

  def insert(self, connection:Type[sqlite3.Connection], taxavalues:Iterable[Tuple[int, str, int]])->None:
    stmt = """INSERT INTO {0} (taxon_id, rank, parent_id) VALUES (?,?,?)
              ON CONFLICT (taxon_id) WHERE parent_id is NULL
              DO UPDATE SET parent_id=excluded.parent_id,rank=excluded.rank""".format(self.name)
    connection.cursor().executemany(stmt, taxavalues)
    connection.commit()

  def insert_taxids(self, connection:Type[sqlite3.Connection], taxids:Iterable[int])->None:
    stmt = """INSERT OR IGNORE INTO {0} (taxon_id) VALUES (?)""".format(self.name)
    connection.cursor().executemany(stmt, taxids)
    connection.commit()

  def get_taxids(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("""SELECT taxon_id FROM {0}""".format(self.name))

  def get_rows(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT taxon_id, rank, name, parent_id FROM {0}".format(self.name))

  def get_lineage(self, connection:Type[sqlite3.Connection], taxid:int, name_table:str)->Type[sqlite3.Cursor]:
    """Recursive construction of lineage from given taxid to highest parent."""
    stmt = """WITH RECURSIVE parent(taxon_id) AS
              (SELECT taxon_id FROM {0} WHERE taxon_id=? UNION ALL
               SELECT t.parent_id FROM {0} t, parent
               WHERE t.taxon_id=parent.taxon_id)
              SELECT t.taxon_id, t.rank, t.parent_id, n.name, n.type FROM {0} t
              JOIN parent p ON t.taxon_id=p.taxon_id
              JOIN {1} n ON t.taxon_id=n.taxon_id""".format(self.name, name_table)
    return connection.cursor().execute(stmt, (taxid,))

  def get_subtree(self, connection:Type[sqlite3.Connection], taxid:int)->Type[sqlite3.Cursor]:
    """Depth first search of taxon ids to find the subtree of taxid"""
    stmt = """WITH RECURSIVE subtree(taxon_id, depth, rank) AS
      (SELECT ti.taxon_id, 0, ti.rank FROM {0} ti WHERE ti.taxon_id=? -- initial lookup
       UNION ALL                                                      -- start recursion
       SELECT tq.taxon_id, st.depth+1, tq.rank FROM {0} tq            -- subquery
       JOIN subtree st ON tq.parent_id=st.taxon_id
       ORDER BY 2 DESC)                                               -- do dfs
       SELECT rst.taxon_id, rst.rank, t.parent_id, n.name, n.type FROM subtree rst -- select recursed results
       JOIN names n on rst.taxon_id=n.taxon_id
       JOIN {0} t on t.taxon_id=rst.taxon_id""".format(self.name)
    return connection.cursor().execute(stmt, (taxid,))
