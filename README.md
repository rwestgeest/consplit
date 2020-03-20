# consplit

A utility to split up svg images created by concepts into multiple images with one layer only.

## Background
Where using concepts to make drawings for presentations and more. We often find ourselves making layered drawings to build up a drawing during a slide show. Exporting all layers as separate images is a tedious exercise. However, exporting all layers at once as an svg images _is_ possible. __Therefore:__

We needed a way to split up an svg image into separate drawings automatically. 

`consplit` does that. It can do it in two modes:

1. __split mode__ (the default) creates a new drawing for each of the layers in the input drawing. Each of the generated drawings contains only one layer. The name of the drawing (and its file) is the original drawing name and the layer name concatenated. 
2. __stack mode__ creates a new drawing for each of the layers in the input drawing. Each of the generated drawings contains an incremental number of drawings. i.e.: The first drawing contains on layer (the first layer), the second contains the first and the second layer, and so on. The last drawing is the same drawing as the original. The naming scheme of the output drawings is just like the naming scheme in split mode.

## Usage

From the help:

```
consplit.py [-h] [-v] [-s] [--png]  
                       [--format-drawing-n-layer | --format-drawing-layer | --format-drawing-n]  
                       [--allow-spaces]  
                       concepts_svg_file

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
    

positional arguments:
  concepts_svg_file     path to the the input svg file

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version and exit
  -s, --stacked         use stacked mode
  --png                 create png as output format

formatting:
  --format-drawing-n-layer
                        format names as <drawing>-<layer-index>-<layer> - the
                        default
  --format-drawing-layer
                        format names as <drawing>-<layer>
  --format-drawing-n    format names as <drawing>-<layer-index>
  --allow-spaces        does not replace spaces by dashes
```