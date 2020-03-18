from hamcrest import assert_that, equal_to
from textwrap import dedent
from consplit.formats.svg import SvgRepo, xml_tree_from, as_drawing, as_layers, as_layer, as_stroke
from consplit.domain import Drawing, Layer, Stroke
from builders import a, validDrawing

class TestSvgRepoReadingFiles:
  def test_creates_a_drawing(self):
    drawing = SvgRepo().read('data/drawing.svg')
    assert_that(drawing.name, equal_to('the_drawing'))

class TestSvgToDrawing:
  xml_tree = xml_tree_from(dedent('''\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920.000000px" height="1080.000000px" version="1.1" viewBox="82 -59 960 540">
      <title>the_drawing</title>
      <desc>Drawing exported from Concepts: Smarter Sketching</desc>
      <g id="Layer1" opacity="1.000"></g>
      <g id="Layer2" opacity="1.000"></g>
    </svg>
    ''').encode('utf-8'))
  def test_creates_a_drawing(self):
    drawing = as_drawing(self.xml_tree)
    assert_that(drawing.name, equal_to('the_drawing'))
    assert_that(drawing.width, equal_to('1920.000000px'))
    assert_that(drawing.height, equal_to("1080.000000px"))
    assert_that(drawing.version, equal_to("1.1"))
    assert_that(drawing.view_box, equal_to("82 -59 960 540"))
  
  def test_creates_a_layer_for_each_layer_in_xml(self):
    drawing = as_drawing(self.xml_tree)
    assert_that(drawing.layers, equal_to(as_layers(self.xml_tree.g)))

class TestSvgToLayer:
  xml_tree = xml_tree_from(dedent('''\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920.000000px" height="1080.000000px" version="1.1" viewBox="82 -59 960 540">
      <title>the_drawing</title>
      <desc>Drawing exported from Concepts: Smarter Sketching</desc>
      <g id="Layer1" opacity="0.500">
        <path id="STROKE_1" opacity="1.000" fill="none" stroke="stroke_color" stroke-width="1" stroke-opacity="1.000" stroke-linecap="round" stroke-linejoin="round" d="sadasd"></path>
        <circle id="STROKE_2" opacity="1.000" fill="fill_color" stroke="stroke_color" stroke-width="2" stroke-opacity="1.000" fill-opacity="1.000" cx="163.503" cy="71.482" r="0.647"></circle>
      </g>
    </svg>
    ''').encode('utf-8'))

  def test_creates_a_stroke_for_each_element_inlayer_in_xml(self):
    xml_layer = the_layer_from(xml_tree_with_one_layer_with(dedent('''\
        <path id="STROKE_1" opacity="1.000" fill="none" stroke="stroke_color" stroke-width="1" stroke-opacity="1.000" stroke-linecap="round" stroke-linejoin="round" d="sadasd"></path>
        <circle id="STROKE_2" opacity="1.000" fill="fill_color" stroke="stroke_color" stroke-width="2" stroke-opacity="1.000" fill-opacity="1.000" cx="163.503" cy="71.482" r="0.647"></circle>
    ''')))
    layer = as_layer(xml_layer)
    assert_that(layer.name, equal_to('Layer1'))
    assert_that(layer.opacity, equal_to('0.500'))
    assert_that(layer.strokes[0], equal_to(as_stroke(xml_layer.path)))
    assert_that(layer.strokes[1], equal_to(as_stroke(xml_layer.circle)))

  def test_stroke_is_an_object_with_a_type_and_all_attributes(self):
    xml_layer = the_layer_from(xml_tree_with_one_layer_with(dedent('''\
        <path id="STROKE_1" opacity="1.000" fill="none" stroke="stroke_color" stroke-width="1" stroke-opacity="1.000" stroke-linecap="round" stroke-linejoin="round" d="sadasd"></path>
    ''')))  
    stroke = as_stroke(xml_layer.path)
    assert_that(stroke.type, equal_to('path'))
    assert_that(stroke.attributes, equal_to({
      'id': "STROKE_1", 
      'opacity': "1.000", 
      'fill': "none", 
      'stroke': "stroke_color", 
      'stroke-width': "1", 
      'stroke-opacity': "1.000", 
      'stroke-linecap': "round", 
      'stroke-linejoin': "round", 
      'd': "sadasd"}))
        
  def test_circle_is_an_object_with_a_type_and_all_attributes(self):
    xml_layer = the_layer_from(xml_tree_with_one_layer_with(dedent('''\
        <circle id="STROKE_2" opacity="1.000" fill="fill_color" stroke="stroke_color" stroke-width="2" stroke-opacity="1.000" fill-opacity="1.000" cx="163.503" cy="71.482" r="0.647"></circle>
    ''')))  
    stroke = as_stroke(xml_layer.circle)
    assert_that(stroke.type, equal_to('circle'))
    assert_that(stroke.attributes, equal_to({
      'id': "STROKE_2", 
      'opacity': "1.000", 
      'fill': "fill_color", 
      'stroke': "stroke_color", 
      'stroke-width': "2", 
      'stroke-opacity': "1.000", 
      'fill-opacity': "1.000", 
      'cx': "163.503", 
      'cy': "71.482", 
      'r': "0.647"}))

def the_layer_from(xml_tree):
  return xml_tree.g[0]

def xml_tree_with_one_layer_with(xml_string):
  return xml_tree_from(dedent('''\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920.000000px" height="1080.000000px" version="1.1" viewBox="82 -59 960 540">
      <title>the_drawing</title>
      <desc>Drawing exported from Concepts: Smarter Sketching</desc>
      <g id="Layer1" opacity="0.500">
        {}
      </g>
    </svg>
    ''').format(xml_string).encode('utf-8'))

class TestSvgRepoWritingFiles:
  def test_writes_a_valid_drawing(self):
    written_drawing = a(validDrawing().withName('written_drawing'))
    SvgRepo().save(written_drawing, 'data')
    read_drawing = SvgRepo().read('data/written_drawing.svg')
    assert_that(read_drawing, equal_to(written_drawing))

