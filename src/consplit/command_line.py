#!/usr/bin/env python
from argparse import ArgumentParser
from consplit.svg import SvgRepo
from consplit.files import location_of
from textwrap import dedent

def usage():
  print(dedent('''\
    consplit [options] path_to_svg

    Where:

      path_to_svg: is the path to the input svg
      options is one of:
      --help,-h:    show this message
      --stacked,-s: use stacked mode
    '''))
  sys.exit(2)

def main():
  parser = ArgumentParser()
  parser.add_argument('concepts_svg_file', help="path to the the input svg file")
  parser.add_argument('-s','--stacked', help="use stacked mode", 
                      action='store_const', const='_stacked', default='')
  args = parser.parse_args()
  
  mode='split' + args.stacked

  repo = SvgRepo()
  drawing = repo.read(args.concepts_svg_file)
  for new_drawing in getattr(drawing, mode)():
    repo.save(new_drawing, location_of(args.concepts_svg_file))

if __name__ == "__main__":
  main()