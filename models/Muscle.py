from models.Base import Base

class Muscle(Base):
  def __init__(self):
    super().__init__()
    self.url_name = "muscle/"
    self._Base__initializator()