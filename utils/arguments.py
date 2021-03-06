#!/usr/bin/env python3

import argparse
from argparse import RawTextHelpFormatter

# Custom usage / help menu.
class HelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = ''
        return super(HelpFormatter, self).add_usage(
            usage, actions, groups, prefix)


def parse_args():
  ''' Define arguments '''
  
  # Custom help menu.
  custom_usage = """
  Usage: 
    python3 usefulShodan2.py <inputfile>
    python3 usefulShodan2.py <inputfile> -d
    python3 usefulShodan2.py <inputfile> -v
    python3 usefulShodan2.py <inputfile> -vv
    
  Positional argument(s):
    [inputfile]: Input from list of IP addresses (supports one IP address per line).

  Optional argument(s):
    [-d, --drop]: Drop existing data and launch with a clean database.
    [-v, --verbose]: Increase verbosity level (Include results 'None').
    [-vv, --verbose --verbose]: Increase verbosity level (Include results 'None' and print results in real-time).
  """
  # Define parser
  parser = argparse.ArgumentParser(formatter_class=HelpFormatter, description='', usage=custom_usage, add_help=False)
  
  # Positional args.
  parser.add_argument('filepath', type=str, metavar='<inputfile>', default='', help='Input from list of IP addresses (supports one IP address per line).')
  
  # Optional argument group.
  optional_group = parser.add_argument_group('optional_args')
  optional_group.add_argument('-d', '--drop', required=False, action='store_true', default='', help='Launch with clean database.')

  # Mutually Exclusive group.
  mutually_exclusive_group = parser.add_mutually_exclusive_group()
  mutually_exclusive_group.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity level (use -vv for greater effect).')
 
  # Initiate parser instance
  args = parser.parse_args()
  return args

def main():
  import arguments
  arguments.parse_args()

if __name__ == "__main__":
    main()
