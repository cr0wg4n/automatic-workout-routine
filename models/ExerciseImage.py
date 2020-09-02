from models.Base import Base

class ExerciseImage(Base):
  def __init__(self):
    super().__init__()
    self.url_name = "exerciseimage/"
    self._Base__initializator()