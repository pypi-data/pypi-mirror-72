## TaxonomyTable
# @ingroup taxonomist
# TaxonomyTable is the main class to deal with NCBI taxonomy SQlite3 tables.
# Table instances are registered by TaxonomyDb. It acts as very simple base
# class.

import sqlite3
from typing import Type

class BaseTable:

  ## Constructor
  # @param name, str, clade name
  # @param database, reference, reference to corresponding SQlite3 instance
  def __init__(self, name:str, database:str):
    self.name = name
    self.database = database
    self.idx = "{}_idx".format(self.name)

  ## Creating table
  # A virtual function
  def create(self, connection:Type[sqlite3.Connection]) -> __qualname__:
    raise NotImplementedError("Implement create() method")

  def create_index(self, connection) -> None:
    raise NotImplementedError("Implement create_index() method")

  ## Getting all rows
  # A virtual function
  def get_rows(self, connection):
    raise NotImplementedError("Help! Implement get_rows() method")

  def insert(self, connection) -> None:
    raise NotImplementedError("Implement insert() method")

  ## Getter function to get static rankmap
  # @returns rankmap, dict
  def get_col_rank(self, rank):
    return self.__class__.rankmap.get(rank, rank)


  def size(self):
    stmt = "SELECT COUNT(id) FROM {0}".format(self.name)
    c = self.database.execute_stmt(stmt)
    return c.fetchone()[0]
