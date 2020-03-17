from consplit.domain import Drawing, Layer, Stroke
from functools import reduce 

class DrawingBuilder:
  def __init__(self, drawing):
    self._drawing = drawing

  def withName(self, name):
    self._drawing = self._drawing.copy(name = name)
    return self

  def withLayer(self, layer):
    self._drawing = self._drawing.copy(layers = self._drawing.layers + [layer])
    return self

  def withLayers(self, *layers):
    self._drawing = self._drawing.copy(layers=list(layers))
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
    layers = [Layer(name='Layer1', strokes=[Stroke(type='path', attributes=dict(d="1212321"))])]
  ))

def a(builder):
  return builder.build()
