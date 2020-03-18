from os import path
from lxml import objectify, etree

class Repo:
  def __init__(self, extension):
    self._extension = extension

  def filepath(self, drawing, location):
    return path.join(location, '{}.{}'.format(drawing.name, self._extension))


def as_svg(drawing):
  E = objectify.ElementMaker(annotate=False, namespace="http://www.w3.org/2000/svg", nsmap ={ None : "http://www.w3.org/2000/svg", 'xlink':"http://www.w3.org/1999/xlink" })
  
  root = E.svg(
    E.title(drawing.name),
    *[ as_svg_layer(E, layer) for layer in drawing.layers ],
    width=drawing.width,
    height=drawing.height,
    version=drawing.version,
    viewBox=drawing.view_box)
  return etree.tostring(etree.ElementTree(root), xml_declaration=True, encoding="UTF-8", standalone="yes", pretty_print=True)

def as_svg_layer(E, layer):
  return E.g(
    * [ as_svg_stroke(E, stroke) for stroke in layer.strokes ],
    id=layer.name, 
    opacity=layer.opacity)

def as_svg_stroke(E, stroke):
  svg_stroke = getattr(E, stroke.type)()
  for (key, val) in stroke.attributes.items():
    svg_stroke.attrib[key] = val
  return svg_stroke

def write_bytes_to(filepath, content):
  with open(filepath, 'w+b') as file:
    return file.write(content)
