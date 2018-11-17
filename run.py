from pprint import pprint
from phue import Bridge
import time
import random
from rgbxy import Converter
import json
import pychromecast

import socket
ip = socket.gethostbyname(socket.gethostname())
print(ip)

from flask import Flask
app = Flask(__name__,static_url_path='/static')

cast_devices = ["Kitchen speaker","Master Bed Room", "Office speaker", "Game Room"]
CAST = {}


ROOMS = {
	"2": {
	"speaker": "Game Room",
	"lights": ["gameroom top", "gameroom top2", "game room left", "game room right", "behind tv"],
	"huelights": []
	}, 
	"1": {
	"speaker": "Office speaker",
	"lights":["outside close to door","outsode under entrance", "outside office", "adress light", "office color", "office white"],
	"huelights": []
	},
	"3": {
	"speaker": "Kitchen speaker",
	"lights":["Kitchen 2", "Kitchen 1", "living room 1", "living room 2"],
	"huelights": []
	},
	"4": {
    "speaker": "Master Bed Room",
    "lights":["Hue color lamp 4", "Hue color lamp 9"],
    "huelights":[]
	},
	"5": {
	"speaker": "Game Room",
	"lights": ["gameroom top", "gameroom top2", "game room left", "game room right", "behind tv"],
	"huelights": []
	}, 
}


def turn_off(lights, time_sleep=2):
	for l in lights:
		l.transitiontime = time_sleep*10
		l.on = False
	time.sleep(time_sleep)

def turn_on(lights, time_sleep=2,brightness=255):
	for l in lights:
		l.brightness = brightness
		l.transitiontime = time_sleep*10
		l.on = True
	#time.sleep(time_sleep)

def change_color(lights, xy):
	for l in lights:
		l.xy = xy

def colors(r=255,g=255,b=255):
	converter = Converter()
	value = converter.rgb_to_xy(r, g, b)
	return [value[0],value[1]]


def pause(time_sleep):
	time.sleep(time_sleep)

COLOR_STATE = {}

def save_color_state(lights):
	global COLOR_STATE

	for l in lights:
		try:
			COLOR_STATE[l.name] = l.xy
		except Exception:
			pass

def restore_color_state(lights,time_sleep=0):
	global COLOR_STATE

	pprint(COLOR_STATE)
	
	for l in lights:
		try:
			pprint(l.xy)
			l.xy = COLOR_STATE[l.name]
			turn_on([l],time_sleep=time_sleep)
		except Exception:
			pass


def flash(maxtime,lights,color=(15000,0)):
	turn_off(lights,.3)
	pause(1)
	start_time = time.time()
	end_time = start_time + maxtime

	while time.time() < end_time:
		numlights = random.randint(0,len(lights)-1)
		time_pause = random.uniform(.1,.5)

		for l in lights:
			l.xy = colors()

		#lights = []

		for i in range(0,numlights):
			time_flash = random.uniform(.1,.4)
			
			selectlight = random.randint(0,len(lights)-1)
			lights[selectlight].transitiontime = int(time_flash*1)
			new_light_state = not lights[selectlight].on
			if new_light_state:
				lights[selectlight].brightness = random.randint(20,255)
				lights[selectlight].on = True
			else:
				lights[selectlight].on = False
		pause(time_pause)


OUTSIDE_SOUNDS = ["outside1.mp3","outside2.mp3", "outside3.wav"]

def playsoundoutside(room="Office speaker"):
	mc = CAST[room].media_controller
	song = random.randint(0,len(OUTSIDE_SOUNDS)-1)

	mc.play_media("http://" + ip + ":5000/static/" + OUTSIDE_SOUNDS[song],content_type='audio/wav' )
	mc.block_until_active()
	mc.play()

def playsound(room):
	mc = CAST[room].media_controller
	mc.play_media("http://" + ip + ":5000/static/rickportal.wav",content_type='audio/wav')
	mc.block_until_active()
	mc.play()




OUTSIDE_LIGHTS = []
LIGHTARRAY = []
LIGHTS = []
PORTAL_LIGHTS = []
PORTALARRAY = []

def connect_bridge():	
	global OUTSIDE_LIGHTS
	global LIGHTARRAY
	global LIGHTS
	global PORTALARRAY
	global ROOMS
	b = Bridge('10.1.1.103')

	b.connect()

	LIGHT1 = 'game room left'
	LIGHT2 = 'game room right'
	LIGHT3 = 'behind tv'
	LIGHT4 = 'gameroom top'
	LIGHT5 = 'gameroom top2'
	LIGHTARRAY = [LIGHT1, LIGHT2, LIGHT3,LIGHT4, LIGHT5]
	PORTALARRAY = LIGHTARRAY

	LIGHTS = b.lights

	for room in ROOMS.keys():
		for l in LIGHTS:
			if l.name in ROOMS[room]["lights"]:
				ROOMS[room]["huelights"].append(l)
			


def setup_cast():
	global CAST
	chromecasts = pychromecast.get_chromecasts()
	for castd in cast_devices:
		CAST[castd] = next(cc for cc in chromecasts if cc.device.friendly_name == castd)
	print("Loaded Cast Devices")
#pprint(lights)

@app.before_first_request
def setup():
	print("Running Setup")
	connect_bridge()
	setup_outside()
	setup_portalgun()
	setup_cast()
	print("Setup Done")

def setup_portalgun():
	global LIGHTS
	global PORTAL_LIGHTS
	global PORTALARRAY
	for l in LIGHTS:
		if l.name in PORTALARRAY:
			pprint(l.name)
			PORTAL_LIGHTS.append(l)

def run_portalgun(lights_to_use):
	global PORTAL_LIGHTS
	save_color_state(lights_to_use)
	change_color(lights_to_use,colors(255,255,255))
	LIGHTS_TO_CHANGE = lights_to_use
	for i in range(0,2):

		turn_off(LIGHTS_TO_CHANGE,time_sleep=0)
		pause(random.randint(1,4)*.1)
		turn_on(LIGHTS_TO_CHANGE,time_sleep=0)
		pause(random.randint(1,4)*.1)
		turn_off(LIGHTS_TO_CHANGE,time_sleep=0)
		pause(random.randint(1,4)*.1)
		turn_on(LIGHTS_TO_CHANGE, time_sleep=0)

	#change_color(LIGHTS_TO_CHANGE, colors(0,255,162))

	for i in range(0,7):
		turn_off(LIGHTS_TO_CHANGE,time_sleep=.3)
		change_color(LIGHTS_TO_CHANGE, colors(0,255,random.randint(0,100)))
		turn_on(LIGHTS_TO_CHANGE,time_sleep=.3)
		change_color(LIGHTS_TO_CHANGE, colors(0,255,random.randint(0,100)))

	change_color(LIGHTS_TO_CHANGE, [0.1938,.6821])
	turn_on(LIGHTS_TO_CHANGE,time_sleep=0)
	pause(10)

	restore_color_state(lights_to_use)

def setup_outside():
	global LIGHTS
	for l in LIGHTS:
		if l.name in LIGHTARRAY:
			OUTSIDE_LIGHTS.append(l)



def run_outside(room):
	#turn_off(OUTSIDE_LIGHTS,time_sleep=4)
	playsoundoutside(room["speaker"])
	save_color_state(room["huelights"])
	turn_off(room["huelights"],time_sleep=2)


	flash(20,room["huelights"])

	turn_on(room["huelights"],time_sleep=0)

	#for l in OUTSIDE_LIGHTS:
	#	random_seed = random.randint(1,2)
	#	print(random_seed)
	#	if random_seed == 1:
	#		l.xy = colors(167,66,244)
	#	elif random_seed == 2:
	#		l.xy = colors(255,69,0)
	#	else:
	#		l.xy = colors(255,69,0)
	#	#l.xy = colors(255,69,0)

	turn_off(room["huelights"],time_sleep=0)
	#pause(4)
	restore_color_state(room["huelights"],time_sleep=10)





@app.route('/outside')
def runoutsideprogram():
	run_outside()
	return "{ 'complete':True, 'status':'ok' }"

@app.route('/portal/<room>')
def runportalprogram(room=1):

	if room == "2" or room == 2 or room == "1" or room == 1:
		run_outside(ROOMS[room])
	else:
		playsound(ROOMS[room]["speaker"])
		run_portalgun(ROOMS[room]["huelights"])
	return "{ 'complete':True, 'status':'ok' }"


@app.route('/lights')
def printrooms():
	global LIGHTS
	lights_hue = []
	for l in LIGHTS:
		lights_hue.append(l.name)
	return json.dumps(lights_hue)



if __name__ == "__main__":
    app.run(host="0.0.0.0")