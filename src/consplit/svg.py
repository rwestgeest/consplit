from lxml import objectify, etree
from consplit.domain import Drawing, Layer, Stroke

def read_bytes_from(filepath):
  with open(filepath, 'rb') as file:
    return file.read()
def write_bytes_to(filepath, content):
  with open(filepath, 'w+b') as file:
    return file.write(content)

def xml_tree_from(string):
  return objectify.fromstring(string)

class SvgRepo:
  def read(self, filepath):
    return as_drawing(xml_tree_from(read_bytes_from(filepath)))

  def save(self, drawing, location):
    write_bytes_to(self.filepath(drawing, location), as_svg(drawing))

  def filepath(self, drawing, location):
    return '{}/{}.svg'.format(location, drawing.name)

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
