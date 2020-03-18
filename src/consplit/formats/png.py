from cairosvg import svg2png
from consplit.formats.repo import Repo, as_svg, write_bytes_to

class PngRepo(Repo):
  def __init__(self):
    super().__init__('png')

  def save(self, drawing, location):
    svg2png(as_svg(drawing), write_to=self.filepath(drawing, location))
