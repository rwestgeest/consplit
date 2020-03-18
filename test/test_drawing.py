from hamcrest import assert_that, equal_to
from consplit.domain import Drawing, Layer
from builders import a, validDrawing

class TestDrawingSplit:
  def test_creates_a_new_drawing_with_layer_name_for_single_layer_drawing(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1')))
    drawings = drawing.split()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-1-Layer1').withLayers(Layer('Layer1')))
    ]))

  def test_splits_into_drawings_named_after_the_layers_with_one_layer_each(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1'), Layer('Layer2')))
    drawings = drawing.split()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-1-Layer1').withLayers(Layer('Layer1'))),
      a(validDrawing().withName('TheDrawing-2-Layer2').withLayers(Layer('Layer2')))
    ]))

class TestDrawingSplitStacked:
  def test_creates_a_new_drawing_with_layer_name_for_single_layer_drawing(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1')))
    drawings = drawing.split_stacked()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-1-Layer1').withLayers(Layer('Layer1')))
    ]))

  def test_splits_into_drawings_named_after_the_layers_where_consecutive_drawings_add_a_layer(self):
    drawing = a(validDrawing()
      .withName('TheDrawing')
      .withLayers(Layer('Layer1'), Layer('Layer2')))
    drawings = drawing.split_stacked()
    assert_that(drawings, equal_to([
      a(validDrawing().withName('TheDrawing-1-Layer1')
        .withLayers(Layer('Layer1'))),
      a(validDrawing().withName('TheDrawing-2-Layer2')
        .withLayers(Layer('Layer1'), Layer('Layer2')))
    ]))