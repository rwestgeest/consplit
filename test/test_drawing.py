from hamcrest import assert_that, equal_to
from concepts.domain import Drawing, Layer

class DrawingBuilder:
  def __init__(self, drawing):
    self._drawing = drawing

  def withName(self, name):
    self._drawing = self._drawing.copy(name = name)
    return self

  def withLayer(self, layer):
    self._drawing = self._drawing.copy(layers = self._drawing.layers + [layer])
    return self
    
  def build(self):
    return self._drawing


def validDrawing():
  return DrawingBuilder(Drawing(
    name = 'someDrawing',
    width = '900px',
    height = '400px',
    version = '2.0',
    view_box = '80 80 80 80',
    layers = []
  ))


def a(builder):
  return builder.build()

class TestDrawingSplit:
  def test_creates_a_new_drawing_with_layer_name_for_single_layer_drawing(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayer(Layer('Layer1')))
    drawings = drawing.split()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-Layer1').withLayer(Layer('Layer1')))
    ]))

  def test_splits_into_drawings_named_after_the_layers_with_one_layer_each(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayer(Layer('Layer1'))
      .withLayer(Layer('Layer2')))
    drawings = drawing.split()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-Layer1').withLayer(Layer('Layer1'))),
      a(validDrawing().withName('TheDrawing-Layer2').withLayer(Layer('Layer2')))
    ]))

class TestDrawingSplitStacked:
  def test_creates_a_new_drawing_with_layer_name_for_single_layer_drawing(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayer(Layer('Layer1')))
    drawings = drawing.split_stacked()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-Layer1').withLayer(Layer('Layer1')))
    ]))

  def test_splits_into_drawings_named_after_the_layers_where_consecutive_drawings_add_a_layer(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayer(Layer('Layer1'))
      .withLayer(Layer('Layer2')))
    drawings = drawing.split_stacked()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-Layer1')
        .withLayer(Layer('Layer1'))),
      a(validDrawing().withName('TheDrawing-Layer2')
        .withLayer(Layer('Layer1'))
        .withLayer(Layer('Layer2')))
    ]))