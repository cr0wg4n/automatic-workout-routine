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
from multiprocessing import Process
from http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 3007
TIME = 60 #minutes
SEX = "male" # "female"
IMAGES = True
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
  
class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    self.path = '/src/' + self.path
    return http.server.SimpleHTTPRequestHandler.do_GET(self)

pp = pprint.PrettyPrinter(indent=1)

def random_limiter(count):
  limit = 0
  offset = 0
  while True:
    limit = randint(0, count-1)
    offset = randint(0, count-1)
    if (limit + offset) < count:
      break
  return (limit, offset)

def launch_serve():
  print("Getting information..")
  name = ""
  description = ""
  video_results = []
  exercise_images= []
  relative_limit = randint(0, 10)
  relative_offset = randint(0, 100)
  count = 0
  image = None
  flag = True
  while flag:
    flag = True
    equipement = randomizer(EQUIPEMENT)
    print("offset:", relative_offset, "limit:", relative_limit, "total:", count, "equipement:", EQUIPEMENT[equipement]["name"])
    equipement_id = EQUIPEMENT[equipement]["id"]
    exercises = Exercise().get_filtered({ "language": 2, "equipment": equipement_id, "limit": relative_limit, "offset": relative_offset})
    relative_limit, relative_offset = random_limiter(exercises.total)
    count = exercises.total
    exercises = exercises.results
    if len(exercises) == 0:
      continue
    if IMAGES:
      for exercise in exercises:
        print(".")
        exercise_images = ExerciseImage().get_filtered({"exercise": exercise["id"]}).results
        if len(exercise_images) > 0:
          description = exercise["description"]
          name = exercise["name"]
          image = exercise_images[0]["image"]
          flag =False
          break
    else:
      exercise = exercises[randomizer(exercises)]
      description = exercise["description"]
      name = exercise["name"]
      break
    print("...")
  
  video_results = YoutubeSearch(name + " {} workout".format(SEX), max_results=9).to_dict()
  data = {
    "title": name,
    "description": description,
    "image": image,
    "videos": video_results
  }

  with open("src/data.js", "w") as text_file:
    data = json.dumps(data)
    data = "const data=" + data
    text_file.write(data)

  handler = HttpRequestHandler
  host = "http://localhost:{}".format(PORT)
  webbrowser.open(host, new=2)
  print("Open at", host)
  server = HTTPServer(server_address=('', PORT), RequestHandlerClass=handler)
  server.serve_forever()

if __name__ == "__main__":
  while True:
    try:
      print('> Start')
      proc = Process(target=launch_serve)
      proc.start()
      time.sleep(TIME * 60)
      proc.terminate()
      proc.kill()
      proc.join()
      print("> Stop")
    except:
      print("Some error :P")
      continue
