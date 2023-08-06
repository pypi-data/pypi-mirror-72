"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
from typing import Dict, Iterable, List, Mapping


from ncbi_taxonomist.model import accession

def read_stdin(sep:str=None) -> List[str]:
  if not sep:
    return [x.strip() for x in sys.stdin]
  args = []
  for i in sys.stdin:
    if sep == ',':
      args += [x.strip() for x in i.replace(' ', '').split(',')]
    else:
      args += [x.strip() for x in i.split(' ')]
  return args

def read_int_stdin(sep:str=None) -> List[int]:
  uniq_taxids = set()
  if not sep:
    uniq_taxids.update([int(x.strip()) for x in sys.stdin])
    return [x for x in uniq_taxids]
  for i in sys.stdin:
    if sep == ',':
      uniq_taxids.update([int(x.strip()) for x in i.replace(' ', '').split(',')])
    else:
      uniq_taxids.update([int(x.strip()) for x in i.replace(' ', '').split(',')])
  return [x for x in uniq_taxids]

def parse_taxids(taxids:Iterable[str]) -> List[int]:
  if taxids is None:
    return None
  if not taxids:
    return read_int_stdin()
  uniq_taxids = set()
  for i in taxids:
    uniq_taxids.update(set([int(x) for x in i.replace(' ', ',').split(',')]))
  return [x for x in uniq_taxids]

def parse_names(names:Iterable[str]) -> List[str]:
  if names is None:
    return None
  if not names:
    return read_stdin()
  args = []
  for i in names:
    args += [x.strip() for x in i.split(',')]
  return args

def json_stdout(data:Mapping[str,str]):
  sys.stdout.write(json.dumps(data)+'\n')

def resolve_log_nspace(cls, rootlogger='ncbi-taxonomist'):
  return "{}.{}.{}".format(rootlogger, cls.__module__, cls.__qualname__)

#def resolve_func_nspace(cls, func, rootlogger='ncbi-taxonomist'):
  #return "{}.{}.{}.{}".format(rootlogger, cls.__module__, cls.__qualname__, sys._getframe().f_code.co_name)
