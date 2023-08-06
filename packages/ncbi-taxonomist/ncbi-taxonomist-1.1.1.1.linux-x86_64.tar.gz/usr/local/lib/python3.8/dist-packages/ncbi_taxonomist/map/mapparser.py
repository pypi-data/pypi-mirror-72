"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import json


from ncbi_taxonomist.model import accession


def parse_accession_map(accs, taxids):
  for i in sys.stdin:
    mapping = json.loads(i.strip())
    if 'accs' not in mapping or 'data' not in mapping:
      sys.exit("Not valid mapping data. Abort.")
    if mapping['data']['taxon_id'] not in taxids:
      taxids[mapping['data']['taxon_id']] = []
    taxids[mapping['data']['taxon_id']].append(mapping['accs'])
    accs[mapping.pop('accs')] = accession.AccessionData.new(mapping['data'])
