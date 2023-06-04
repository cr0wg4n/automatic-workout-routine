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
from http.server import HTTPServer
from config import (
  PORT,
  TIME,
  SEX,
  IMAGES,
  MAX_YT_RESULTS,
  EQUIPMENT
)

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
    equipement = randomizer(EQUIPMENT)
    print("offset:", relative_offset, "limit:", relative_limit, "total:", count, "equipement:", EQUIPMENT[equipement]["name"])
    equipement_id = EQUIPMENT[equipement]["id"]
    # Language id 2 is english, https://wger.de/api/v2/language/
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
  
  video_results = YoutubeSearch(
      "{} {} workout at home".format(name, SEX), 
      max_results=MAX_YT_RESULTS
    ).to_dict()

  data = {
    "title": name,
    "description": description,
    "image": image,
    "videos": video_results
  }

  with open('src/data.js', 'w') as text_file:
    data = json.dumps(data)
    data = "const data=" + data
    text_file.write(data)

  handler = HttpRequestHandler
  host = "http://localhost:{}".format(PORT)
  print("Open at", host)
  server = HTTPServer(server_address=('', PORT), RequestHandlerClass=handler)
  webbrowser.open(host, new=2)
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
    except Exception as error:
      print("Some error:", error)
      continue
