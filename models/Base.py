from urllib.parse import urljoin
import requests

class Base():
  def __init__(self):
    self.base_url = "https://wger.de/api/v2/"
    self.url_name = ""
    self.headers = {'Accept': 'application/json'}

  def get_menu(self):
    return requests.get(self.base_url, timeout=2).json()

  def __get_by_id(self, _id=""):
    url = urljoin(self.pseudo_base_url, (str(_id)))
    response = requests.get(url, timeout=2).json()
    return response
  
  def __get_list(self, filters=None):
    if filters:
      raw_filters = "?"
      aux = 0
      for key in filters:
        aux +=1
        raw = "{}={}".format(key, filters[key])
        if (aux != len(filters)):
          raw += "&"
        raw_filters += raw
      url = urljoin(self.pseudo_base_url, raw_filters)
    else:
      url = self.pseudo_base_url
    response = requests.get(url, timeout=3).json()["results"]
    return response

  def __initializator(self):
    self.pseudo_base_url = urljoin(self.base_url, self.url_name)
    
  def get_id(self, _id):
    return self.__get_by_id(_id)

  def get_all(self):
    return self.__get_list()

  def get_filtered(self, filters):
    return self.__get_list(filters)

