from pprint import pprint
from phue import Bridge
import time
import random
from rgbxy import Converter

def turn_off(time_sleep=2):
	for l in HUELIGHTS:
		l.transitiontime = time_sleep*10
		l.on = False
	time.sleep(time_sleep)

def turn_on(time_sleep=2):
	for l in HUELIGHTS:
		l.brightness = 255
		l.transitiontime = time_sleep*10
		l.on = True
	time.sleep(time_sleep)

def change_color(xy):
	for l in HUELIGHTS:
		l.xy = xy

def colors(r=255,g=255,b=255):
	converter = Converter()
	value = converter.rgb_to_xy(r, g, b)
	return [value[0],value[1]]


def pause(time_sleep):
	time.sleep(time_sleep)


def flash(maxtime, color=(15000,0)):
	turn_off(.3)
	pause(1)
	start_time = time.time()
	end_time = start_time + maxtime

	while time.time() < end_time:
		numlights = random.randint(0,len(HUELIGHTS)-1)
		time_pause = random.uniform(.1,.5)

		for l in HUELIGHTS:
			l.xy = colors()

		lights = []

		for i in range(0,numlights):
			time_flash = random.uniform(.1,1)
			
			selectlight = random.randint(0,len(HUELIGHTS)-1)
			HUELIGHTS[selectlight].transitiontime = int(time_flash*1)
			new_light_state = not HUELIGHTS[selectlight].on
			if new_light_state:
				HUELIGHTS[selectlight].brightness = random.randint(20,255)
				HUELIGHTS[selectlight].on = True
			else:
				HUELIGHTS[selectlight].on = False


		pause(time_pause)








		

b = Bridge('10.1.1.103')

b.connect()

LIGHT1 = 'Hue bloom 1'
LIGHT2 = 'Hue bloom 2'
LIGHT3 = 'Hue color lamp 8'
LIGHTARRAY = [LIGHT1, LIGHT2, LIGHT3]

HUELIGHTS = []

lights = b.lights

for l in lights:
	if l.name in LIGHTARRAY:
		HUELIGHTS.append(l)


pprint(LIGHTARRAY)


turn_off(time_sleep=4)

turn_on(time_sleep=4)


flash(60)

turn_on(time_sleep=0)

for l in HUELIGHTS:
	l.xy = colors(255,69,0)
	l.xy = colors(255,69,0)
	l.xy = colors(255,69,0)
	l.xy = colors(255,69,0)

turn_off()
pause(4)



turn_on(time_sleep=10)