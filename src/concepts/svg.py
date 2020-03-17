from lxml import objectify, etree
from concepts.domain import Drawing, Layer, Stroke

def read_bytes_from(filepath):
  with open(filepath, 'rb') as file:
    return file.read()

def xml_tree_from(string):
  return objectify.fromstring(string)

class SvgDrawing:
  def read(self, filepath):
    return as_drawing(xml_tree_from(read_bytes_from(filepath)))

def as_drawing(svg_drawing):
    return Drawing(
      name=svg_drawing.title, 
      width=svg_drawing.attrib['width'], 
      height=svg_drawing.attrib['height'], 
      version=svg_drawing.attrib['version'], 
      view_box=svg_drawing.attrib['viewBox'], 
      layers=as_layers(svg_drawing.g))

def as_layers(g_elements):
  return [as_layer(svg_layer) for svg_layer in g_elements]

def as_layer(svg_layer_element):
  return Layer(
    name=svg_layer_element.attrib['id'],
    opacity=svg_layer_element.attrib['opacity'],
    strokes=[ as_stroke(xml_stroke) for xml_stroke in svg_layer_element.iterchildren() ]
    )
def as_stroke(svg_stroke_element):
  return Stroke(
    type = etree.QName(svg_stroke_element).localname,
    attributes = svg_stroke_element.attrib)
