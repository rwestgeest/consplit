from dataclasses import dataclass, field, replace
from typing import List, Dict
from functools import reduce
class ValueObject:
  def copy(self, **replacements):
    return replace(self, **replacements)

@dataclass
class Stroke(ValueObject):
  type: str = 'path'
  attributes: Dict = field(default_factory=dict)

@dataclass  
class Layer(ValueObject):
  name: str
  opacity: str = "1.000"
  strokes: List[Stroke] = field(default_factory=list)

@dataclass(frozen=True)
class Drawing(ValueObject):
  name: str
  width: str
  height: str
  version: str
  view_box: str
  layers: List[Layer] = field(default_factory=list)

  def split(self):
    return [ self.copy( 
      name='{}-{}'.format(self.name, layer.name),
      layers=[layer] 
      ) for layer in self.layers ]

  def split_stacked(self):
    drawings = []
    layers = []
    for layer in self.layers:
      layers = layers + [layer]
      drawings.append(self.copy(
        name='{}-{}'.format(self.name, layer.name),
        layers=layers))
    return drawings