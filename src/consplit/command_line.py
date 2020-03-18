#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from consplit.formats import SvgRepo, PngRepo
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
  parser = ArgumentParser(description='''\
    Splits up concepts drawing so that each layer is in its own drawing.

    Works in two modes: 
    1. Split mode (the default) creates a new drawing for each of the 
       layers in the input drawing. 
       Each of the generated drawings contains only one layer. 
       The name of the drawing (and its file) is the original drawing name 
       and the layer name concatenated. 
    2. Stacked mode creates a new drawing for each of the layers in the 
       input drawing. Each of the generated drawings contains an incremental 
       number of layers. i.e.: The first drawing contains on layer (the 
       first layer), the second contains the first and the second layer, 
       and so on. The last drawing is the same drawing as the original. 
       The naming scheme of the output drawings is just like the naming 
       scheme in split mode.
    ''',
    formatter_class=RawDescriptionHelpFormatter)
  parser.add_argument('concepts_svg_file', help="path to the the input svg file")
  parser.add_argument('-s','--stacked', help="use stacked mode", 
                      action='store_const', const='_stacked', default='')
  parser.add_argument('--png', help="create png as output format", 
                      action='store_const', const='store_true')
  args = parser.parse_args()
  
  mode='split' + args.stacked

  repo = SvgRepo()
  output_repo = args.png and PngRepo() or repo
  drawing = repo.read(args.concepts_svg_file)
  for new_drawing in getattr(drawing, mode)():
    output_repo.save(new_drawing, location_of(args.concepts_svg_file))

if __name__ == "__main__":
  main()