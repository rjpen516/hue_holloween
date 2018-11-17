from gpiozero import LED, Button
from time import sleep
import random
import requests
from requests_futures.sessions import FuturesSession

session = FuturesSession()

SERVER_IP = "10.1.1.101"
SERVER_PORT = "5000"


leds = {}
button = {}



def setup():
        leds['ray1'] = LED(2)
        leds['ray2'] = LED(3)
        leds['ray3'] = LED(4)
        leds['screen'] = LED(5)
        leds['rock'] = LED(6)
        button['main'] = Button(7)


def flashray():
        rayarray = ['ray1', 'ray2', 'ray3']

        lucky_on = random.randint(0,5)
        led = random.randint(0,len(rayarray)-1)
        leds[rayarray[led]].toggle()
        if lucky_on == 5:
                for l in rayarray:
                        leds[l].on()

def update_array(num):
	rayarray = ['ray1', 'ray2', 'ray3']
	bit1 = num & 0x01
	bit2 = num & 0x02
	bit3 = num & 0x04

	for bit in rayarray:
		leds[bit].off()

	if bit1:
		leds[rayarray[0]].on()
	if bit2:
		leds[rayarray[1]].on()
	if bit3:
		leds[rayarray[2]].on()


def flashrock():
        led = 'rock'

        leds[led].toggle()

def flashscreen():
        led = 'screen'
        leds[led].toggle()


def run_portal():
        for i in range(0,500):
                for l in range(0,10):
                        flashray()
                if i%7 == 0:
                        flashrock()
                if i%17 == 0:
                        flashscreen()
                sleep(.02)


def all_off():
	for value in leds:
		leds[value].off()

def call_room(room):
	session.get('http://' + SERVER_IP + ":" + SERVER_PORT + "/portal/" + room)

setup()


current_room = "1"

press_counter = 1
button_state = False
room_num = 1
while True:
         if button['main'].is_pressed:
         	press_counter += 1
         elif press_counter > 10:
         	room_num += 1
         	if room_num > 5:
         		room_num = 1
         	print("Room Picker" + str(room_num))
         	print("Button Hold Time" + str(press_counter))
         	update_array(room_num)
         	press_counter = 1
         elif press_counter <= 10 and press_counter > 1:
            print("Button HOld Time" + str(press_counter))
            call_room(str(room_num))
            run_portal()
            all_off()
            press_counter = 1
         sleep(.05)

