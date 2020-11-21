from evdev import InputDevice, categorize, ecodes
from select import select
from yaml import safe_load
from subprocess import Popen
from os import path
from time import sleep

DEVICE = '/dev/input/by-id/usb-Logitech_Gaming_Mouse_G600_1836A07F43730017-if01-event-kbd'

MAP = {
	50: ("G7", False),
	44: ("G8", False),
	2: ("G9", False),
	3: ("G10", False),
	4: ("G11", False),
	5: ("G12", False),
	6: ("G13", False),
	7: ("G14", False),
	8: ("G15", False),
	9: ("G16", False),
	10: ("G17", False),
	11: ("G18", False),
	12: ("G19", False),
	13: ("G20", False),
	24: ("SCROLL-LEFT", False),
	25: ("SCROLL-RIGHT", False),
	
	-1: ("G7", True),
	16: ("G8", True),
	30: ("G9", True),
	48: ("G10", True),
	46: ("G11", True),
	32: ("G12", True),
	18: ("G13", True),
	33: ("G14", True),
	34: ("G15", True),
	35: ("G16", True),
	23: ("G17", True),
	36: ("G18", True),
	37: ("G19", True),
	38: ("G20", True),
	19: ("SCROLL-LEFT", True),
	31: ("SCROLL-RIGHT", True),
}

STATE_MAP = {
	1: "down",
	2: "held",
	0: "up"
}


def handle(code, state):
	try:
		with open('config.yml', 'r') as f:
			config = safe_load(f)
	except OSError:
		config = None
	if config is None:
		print("No config!")
	key, mod = MAP[code]
	state = STATE_MAP[state]
	print(f"handling key: {key}, mod: {mod}, state: {state}")
	try:
		conf = config[key]
		if mod:
			conf = conf['mod']
		command = conf[state]
		print(f"executing: {command}")
		Popen(command, shell=True)
	except KeyError:
		print("executing: nothing")
	except TypeError as e:
		print("config probably invalid", e)
	print()


def handle_loop():
	try:
		dev = InputDevice(DEVICE)
		print("device connected")

		with dev.grab_context():
			while True:
				select([dev], [], [])
				for event in dev.read():
					if event.type == ecodes.EV_KEY:
						handle(event.code, event.value)
				# print(MAP[event.code])
	except OSError as e:
		print("device disconnected", e)


def main_loop():
	while True:
		if path.exists(DEVICE):
			handle_loop()
		else:
			sleep(3)


if __name__ == '__main__':
	main_loop()
