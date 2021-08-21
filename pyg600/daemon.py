from evdev import InputDevice, ecodes
from select import select
from subprocess import run
from os import path
from time import sleep

from .config import Config
from . import constants


class Daemon:
    def __init__(self, config: Config):
        self.config = config

    def start(self):
        while True:
            if path.exists(self.config.device):
                self.handle_loop()
            else:
                sleep(3)

    def handle_loop(self):
        try:
            dev = InputDevice(self.config.device)
            print("device connected")

            with dev.grab_context():
                while True:
                    select([dev], [], [])
                    for event in dev.read():
                        if event.type == ecodes.EV_KEY:
                            self.handle(event.code, event.value)
        except OSError as e:
            print("device disconnected", e)

    def handle(self, code, state):
        key, mod = constants.SHIFT_MAP[code]
        state = constants.STATE_MAP[state]
        print(f"handling key: {key}, mod: {mod}, state: {state}")
        conf = self.config.key_configs.get(key)
        if conf is None:
            return
        command = conf.get_command(state, mod)
        if command is None:
            return
        print(f"executing: {command}")
        run(command, shell=True)
        print()


def start():
    config = Config()
    daemon = Daemon(config)
    daemon.start()
