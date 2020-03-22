from abc import ABC, abstractmethod

def format_name_as(formatter_builder):
  return formatter_builder.build()

def drawing_number_layer():
  return FormatterBuilder(DrawingNumberLayerFormatter())

def drawing_number():
  return FormatterBuilder(DrawingNumberFormatter())

def drawing_layer():
  return FormatterBuilder(DrawingLayerFormatter())

class FormatterBuilder:
  def __init__(self, formatter):
    self._formatter = formatter
    self._wrapper = SpacedFormatterDecorator(self._formatter)

  def without_spaces(self):
    self._wrapper = NoSpacedFormatterDecorator(self._formatter)
    return self

  def with_spaces(self):
    self._wrapper = SpacedFormatterDecorator(self._formatter)
    return self

  def lower_case(self):
    self._wrapper = DownCaseFormatterDecorator(self._formatter)
    return self

  def build(self):
    return self._wrapper

class DrawingNumberLayerFormatter:
  def format(self, drawing, layer_index, layer):
    return '{name}-{layer_no}-{layer_name}'.format(name=drawing.name, layer_no=layer_index+1, layer_name=layer.name)

class DrawingNumberFormatter:
  def format(self, drawing, layer_index, layer):
    return '{name}-{layer_no}'.format(name=drawing.name, layer_no=layer_index+1)

class DrawingLayerFormatter:
  def format(self, drawing, layer_index, layer):
    return '{name}-{layer_name}'.format(name=drawing.name, layer_name=layer.name)

class FormatterDecorator(ABC):
  def __init__(self, wrapped_formatter):
    self._wrapped_formatter = wrapped_formatter

  def format(self, drawing, layer_index, layer):
    return self.decorate(self._wrapped_formatter.format(drawing, layer_index, layer))
  
  @abstractmethod
  def decorate(self, formatted_name):pass

class SpacedFormatterDecorator(FormatterDecorator):
  def decorate(self, formatted_name):
    return formatted_name

class NoSpacedFormatterDecorator(FormatterDecorator):
  def decorate(self, formatted_name):
    return formatted_name.replace(' ', '-')

class DownCaseFormatterDecorator(FormatterDecorator):
  def decorate(self, formatted_name):
    return formatted_name.lower()

