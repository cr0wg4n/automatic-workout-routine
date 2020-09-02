from models.Muscle import Muscle
from models.Exercise import Exercise
from models.ExerciseImage import ExerciseImage
from youtube_search import YoutubeSearch
from random import randint
import json
import time
import pprint 
import webbrowser
import http.server
import socketserver
import threading

PORT = 3004
TIME = 60
EQUIPEMENT = [
  # {
  #   "id": 1,
  #   "name": "Barbell" # barra con pesas largas
  # },
  {
    "id": 8,
    "name": "Bench" # banca, improvisa con una silla común
  },
  {
    "id": 3,
    "name": "Dumbbell" # pesa común, improvisa con una mochila vieja, llenala de libros y cosas pesadas, alternativamente siempre hay una silla mejor si es de metal
  },
  {
    "id": 4,
    "name": "Gym mat" # tapete de gimnasia, ulala, improvisa con un tapete común :P
  },
  # {
  #   "id": 9,
  #   "name": "Incline bench" # banca de inclinación
  # },
  {
    "id": 10,
    "name": "Kettlebell" # pesa rusa, improvisa con una mochila vieja, llenala de libros y cosas pesadas
  },
  {
    "id": 7,
    "name": "none (bodyweight exercise)" # ningún material para ejercitarte, calistenia
  },
  {
    "id": 6,
    "name": "Pull-up bar" # barra para colgarte, improvisa con el marco de tu puerta 
  },
  # {
  #   "id": 5,
  #   "name": "Swiss Ball" # pelota rusa, o la pelota esa de los videos en los que dos sujetos colisionan
  # },
  {
    "id": 2,
    "name": "SZ-Bar" # una barra sin pesas, improvisa con cualquier barra
  }
]

def randomizer(array):
  if len(array)!=0:
    return randint(0,(len(array)-1))
  else:
    return 0
  
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    self.path = '/src/' + self.path
    return http.server.SimpleHTTPRequestHandler.do_GET(self)

pp = pprint.PrettyPrinter(indent=1)

def launch_serve():
  name = ""
  description = ""
  video_results = []
  exercise_images= []
  while True:
    equipement_id = randomizer(EQUIPEMENT)
    equipement_id = EQUIPEMENT[equipement_id]["id"]
    exercises = Exercise().get_filtered({ "language": 2, "equipment": equipement_id}) 
    random_exercise = randomizer(exercises)
    random_exercise = exercises[random_exercise]
    description = random_exercise["description"]
    name = random_exercise["name"]
    exercise_images = ExerciseImage().get_filtered({"exercise": random_exercise["id"]})
    if len(exercise_images) > 0:
      break
  
  video_results = YoutubeSearch(name, max_results=12).to_dict()
  data = {
    "title": name + " workout",
    "description": description,
    "image": exercise_images[0]["image"],
    "videos": video_results
  }

  with open("src/data.js", "w") as text_file:
    data = json.dumps(data)
    data = "const data=" + data
    text_file.write(data)

  handler = MyHttpRequestHandler

  with socketserver.TCPServer(("", PORT), handler) as httpd:
    webbrowser.open("http://localhost:{}".format(PORT), new=2)
    httpd.serve_forever()


while True:
  print('init')
  launch_serve()
  time.sleep(TIME * 60)
