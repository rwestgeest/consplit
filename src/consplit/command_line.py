#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from consplit.formatters import format_name_as, drawing_number_layer, drawing_layer, drawing_number
from consplit.formats import SvgRepo, PngRepo
from consplit.files import location_of
from consplit.version import version
from textwrap import dedent

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
  parser.add_argument('-v','--version', help="show version and exit", 
                      action='version', version='consplit {}'.format(version))
  parser.add_argument('-s','--stacked', help="use stacked mode", 
                      action='store_const', const='_stacked', default='')
  parser.add_argument('--png', help="create png as output format", 
                      action='store_const', const='store_true')
  formatting_group = parser.add_argument_group('formatting')
  name_formatting_group = formatting_group.add_mutually_exclusive_group()
  name_formatting_group.add_argument('--format-drawing-n-layer', help="format names as <drawing>-<layer-index>-<layer> - the default", 
                      action='store_true')
  name_formatting_group.add_argument('--format-drawing-layer', help="format names as <drawing>-<layer>", 
                      action='store_true')
  name_formatting_group.add_argument('--format-drawing-n', help="format names as <drawing>-<layer-index>", 
                      action='store_true')
  formatting_group.add_argument('-l', '--lower-case', help="make file names lower case", 
                      action='store_true')
  formatting_group.add_argument('--allow-spaces', help="does not replace spaces by dashes", 
                      action='store_true')
  args = parser.parse_args()

  formatter=args.format_drawing_n and drawing_number() or (args.format_drawing_layer and drawing_layer() or drawing_number_layer())
  formatter=args.allow_spaces and formatter.with_spaces() or formatter.without_spaces()
  formatter=args.lower_case and formatter.lower_case() or formatter
  
  mode='split' + args.stacked

  repo = SvgRepo()
  output_repo = args.png and PngRepo() or repo
  drawing = repo.read(args.concepts_svg_file)
  for new_drawing in getattr(drawing, mode)(format_name_as(formatter)):
    output_repo.save(new_drawing, location_of(args.concepts_svg_file))

if __name__ == "__main__":
  main()