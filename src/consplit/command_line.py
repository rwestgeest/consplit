#!/usr/bin/env python
from svg import SvgDrawing

svg_drawing = SvgDrawing()
for drawing in svg_drawing.read('data/Collaborate-on-stories.svg').split(): 
  svg_drawing.save(drawing, 'data')