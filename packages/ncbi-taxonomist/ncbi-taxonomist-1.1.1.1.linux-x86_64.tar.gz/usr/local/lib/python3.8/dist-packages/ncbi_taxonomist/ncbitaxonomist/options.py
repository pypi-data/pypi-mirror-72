"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import sys
import argparse


def version(basename):
  vfile=os.path.join((os.path.dirname(os.path.relpath(__file__))), '..', 'VERSION')
  if not os.path.exists(vfile):
    return "{} version: unknown".format(basename)
  fh = open(vfile, 'r')
  version = fh.readline().strip()
  fh.close()
  return "{} version: {}".format(basename, version)

def summary(args):
  runstat = args.command
  if args.taxids:
    runstat += "|taxids"
  if args.names:
    runstat += "|names"
  if args.accessions is not None:
    runstat += "|accessions"
  if args.remote:
    runstat += "|remote"
  if args.database:
    runstat += "|local"
  return runstat

def parse_options(basename):
  ap = argparse.ArgumentParser(add_help=False,
                               epilog="{} <command> -h lists command specific options".format(basename))
  ap._positionals.title = 'commands'  # Not very clean, but whatddya want to do?
  ap.add_argument('--version',
                  action='store_true',
                  help='Show version and exit')

  db = argparse.ArgumentParser(add_help=False)
  db.add_argument('-db', '--database',
                  type=str,
                  default=None,
                  metavar='<path>',
                  help="Path to local database")

  taxa = argparse.ArgumentParser(add_help=False)
  taxa.add_argument('-t', '--taxids',
                    type=str,
                    nargs='*',
                    default=None,
                    metavar='<taxid>',
                    help='Comma / space separated taxids')
  taxa.add_argument('-n', '--names',
                    type=str,
                    nargs='*',
                    default=None,
                    metavar='<name>',
                    help='Comma separated names: \'Homo sapiens, Influenza B virus (B/Acre/121609/2012)\'')

  mapping = argparse.ArgumentParser(add_help=False)


  remote = argparse.ArgumentParser(add_help=False)
  remote.add_argument('-r', '--remote',
                      action='store_true',
                      default=False,
                      help='Use Entrez server')

  email = argparse.ArgumentParser(add_help=False)
  email.add_argument('-e', '--email',
                     type=str,
                     default=None,
                     metavar='<email>',
                     help='Email, required for remote queries')

  subparsers = ap.add_subparsers(dest='command')
  mapper = subparsers.add_parser('map',
                                 help='map taxid to names and vice-versa',
                                 parents=[taxa, db, remote, email])
  mapper.add_argument('-a', '--accessions',
                       type=str,
                       nargs='*',
                       default=None,
                       metavar='<accs>',
                       help='Map accessions to taxa')
  mapper.add_argument('-edb', '--entrezdb',
                      type=str,
                      metavar='<entrezdb>',
                      default='nucleotide',
                      help='Entrez database for accessions. Default: nucleotide')

  resolve = subparsers.add_parser('resolve',
                                  help='resolve lineage',
                                  parents=[taxa, mapping, db, remote, email])
  resolve.add_argument('-m', '--mapping',
                       default=False,
                       action='store_true',
                       help='Resolve accessions mapping result from map via STDIN')
  importer = subparsers.add_parser('import',
                                    help='import taxa into SQLite database',
                                    parents=[db])
  importer.add_argument('-l', '--lineage',
                        default=False,
                        action='store_true',
                        help='import lineages from resolve via STDIN')
  importer.add_argument('-f', '--filter',
                        default=None,
                        type=str,
                        metavar='<attribute>',
                        help='Set attribute to print to STDOUT after import: accs, taxid, lin')

  extractor = subparsers.add_parser('subtree',
                                     help='extract taxa subtree',
                                     parents=[taxa, db, remote])

  collect = subparsers.add_parser('collect',
                                  help='collect taxa information for taxid/names',
                                  parents=[taxa, email]).set_defaults(database=None)

  #ap.add_argument('--import_taxdb',
                  #type=str,
                  #default=None,
                  #metavar='PATH',
                  #help='import taxonomic data from NCBI taxdump file (download separately)')
  ##ap.add_argument('--group', '-g',
                  ##type=str,
                  ##default=None,
                  ##help='create taxonomic group',
                  ##metavar='GROUP')
  #ap.add_argument('-r', '--rank',
                  #type=str,
                  #default=None,
                  #help='phylogenetic rank',
                  #metavar='')
  #ap.add_argument('--add-group', '-ag',
                  #type=str,
                  #default=None,
                  #help='create new taxonomic group',
                  #metavar='GROUPNAME')
  #ap.add_argument('--update-group', '-ug',
                  #type=str,
                  #default=None,
                  #help='create new taxonomic group',
                  #metavar='GROUPNAME')

  if len(sys.argv) == 1:
    ap.print_help()
    sys.exit(0)
  args = ap.parse_args()
  if args.version:
    print(version(basename))
    sys.exit(0)
  return args
