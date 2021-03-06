from dataclasses import dataclass, field, replace
from typing import List, Dict
from functools import reduce
from itertools import accumulate


class ValueObject:
  def copy(self, **replacements):
    return replace(self, **replacements)

@dataclass(frozen=True)
class Stroke(ValueObject):
  type: str = 'path'
  attributes: Dict = field(default_factory=dict)

@dataclass(frozen=True)
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

  def split(self, name_formatter):
    return [ self.copy( 
      name = name_formatter.format(self, i, layer),
      layers=[layer] 
      ) for i, layer in enumerate(self.layers) ]

  def split_stacked(self, name_formatter):
    return [ self.copy(
      name = name_formatter.format(self, i, layer_list[-1]),
      layers = layer_list
    ) for i, layer_list in enumerate(reduce(rollup_layers, self.layers, []))]

def rollup_layers(lists_of_layers, layer):
  if len(lists_of_layers) == 0: return [[layer]]
  return lists_of_layers + [lists_of_layers[-1] + [layer]]

