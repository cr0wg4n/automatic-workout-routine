# Workout Spamer Script
This project was made for people who to want improve their physical skills, the script open a new tab in your default browser every certain time, showing a workout 
exercise, name, description and youtube videos.

## We learn about
* Basic html, css and javascript concepts
* Python built-in basic HTTP server
* Request to API
* Inheritance and object oriented programming
* Video data extraction (youtube library)

## API 
The root endpoint:
```
https://wger.de/api/v2/
```
[WGER](https://wger.de/es/software/features) thanks a lot!

## Execution

```bash
pip install -r requirements.txt
python main.py
```

Alternativement you can customize the script: The port to serve the low-weight-page, time in minutes (every certain time, the page will open in your browser by default), sex (female or male), if you don't need images the image option will be `False` or maybe `True`, you can comment or uncomment the equipement array, depends on what kind of equipement you have.

```python
PORT = 3007
TIME = 60 # minutes
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
```
lol, sorry for my comments in spanish.

## Autostart
This option allow you boot the script after your OS's boot

### Linux
In linux is so easy thanks to `crontab`:
```
```

### Windows
In Windows is a litle bit more complicate, maybe later I making a tutorial.


## Preview
<img alt="Demo " src="https://raw.githubusercontent.com/cr0wg4n/automatic-workout-routine/master/assets/preview.PNG"/>
<br>
Enjoy it!

## Next Steps 
[ ] Selection of the most convenient days and hour, not only all day
