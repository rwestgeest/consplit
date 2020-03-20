from hamcrest import assert_that, equal_to
from consplit.domain import Drawing, Layer
from consplit.formatters import format_name_as, drawing_number_layer, drawing_number, drawing_layer, FormatterBuilder
from builders import a, validDrawing

class BaseSplitTest:
  def format(self, drawing, index, layer):
    return '{}-{}-{}'.format(drawing.name, index, layer.name)

class TestDrawingSplit(BaseSplitTest):
  
  def test_creates_a_new_drawing_formatted_name_for_single_layer_drawing(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1')))
    drawings = drawing.split(self)
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-0-Layer1').withLayers(Layer('Layer1')))
    ]))

  def test_splits_into_drawings_named_after_the_layers_with_one_layer_each(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1'), Layer('Layer2')))
    drawings = drawing.split(self)
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-0-Layer1').withLayers(Layer('Layer1'))),
      a(validDrawing().withName('TheDrawing-1-Layer2').withLayers(Layer('Layer2')))
    ]))


class TestDrawingSplitStacked(BaseSplitTest):
  def test_creates_a_new_drawing_with_layer_name_for_single_layer_drawing(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1')))
    drawings = drawing.split_stacked(self)
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-0-Layer1').withLayers(Layer('Layer1')))
    ]))

  def test_splits_into_drawings_named_after_the_layers_where_consecutive_drawings_add_a_layer(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1'), Layer('Layer2')))
    drawings = drawing.split_stacked(self)
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-0-Layer1')
        .withLayers(Layer('Layer1'))),
      a(validDrawing().withName('TheDrawing-1-Layer2')
        .withLayers(Layer('Layer1'), Layer('Layer2')))
    ]))

class TestDrawingIndexLayerFormatter:
  def test_formats_drawing_name_one_based_index_and_layer_name(self):
    f=format_name_as(drawing_number_layer())
    assert_that(f.format(drawing_with_name('DrawingName'), 3, layer_with_name('Layer Name')), equal_to('DrawingName-4-Layer Name'))
    assert_that(f.format(drawing_with_name('Drawing Name'), 3, layer_with_name('LayerName')), equal_to('Drawing Name-4-LayerName'))
  
class TestDrawingIndexFormatter:
  def test_formats_drawing_name_one_based_index_and_layer_name(self):
    f=format_name_as(drawing_number())
    assert_that(f.format(drawing_with_name('DrawingName'), 3, layer_with_name('Layer Name')), equal_to('DrawingName-4'))
    assert_that(f.format(drawing_with_name('Drawing Name'), 3, layer_with_name('LayerName')), equal_to('Drawing Name-4'))

class TestDrawingLayerFormatter:
  def test_formats_drawing_name_one_based_index_and_layer_name(self):
    f=format_name_as(drawing_layer())
    assert_that(f.format(drawing_with_name('DrawingName'), 3, layer_with_name('Layer Name')), equal_to('DrawingName-Layer Name'))
    assert_that(f.format(drawing_with_name('Drawing Name'), 3, layer_with_name('LayerName')), equal_to('Drawing Name-LayerName'))

class TestNoSpacedWrapper:
  def format(self, drawing, index, layer):
    return "So very much  spaces"
  def test_replaces_spaces_with_dashes(self):
    f=format_name_as(FormatterBuilder(self).without_spaces())
    assert_that(f.format(None, 0, None), equal_to("So-very-much--spaces"))

class TestSpacedWrapper:
  def format(self, drawing, index, layer):
    return "So very much  spaces"
  def test_replaces_spaces_with_dashes(self):
    f=format_name_as(FormatterBuilder(self).with_spaces())
    assert_that(f.format(None, 0, None), equal_to("So very much  spaces"))


def drawing_with_name(name):
  return a(validDrawing().withName(name))

def layer_with_name(name):
  return Layer(name=name)