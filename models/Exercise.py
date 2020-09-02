from models.Base import Base

class Exercise(Base):
  def __init__(self):
    super().__init__()
    self.url_name = "exercise/"
    self._Base__initializator()