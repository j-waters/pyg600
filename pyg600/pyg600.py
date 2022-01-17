from subprocess import Popen

from pymacropad import Daemon, KeyEvent

from .config import Config, ModKeyConfig
from .constants import SHIFT_MAP


def start():
    config = Config()

    def handle(event: KeyEvent):
        key, is_mod = SHIFT_MAP[event.key]
        key_conf: ModKeyConfig = config.key_configs.get(key)
        if key_conf is None:
            return
        command = key_conf.get_command_with_mod(event.state, is_mod)
        if command is not None:
            Popen(command, shell=True)

    daemon = Daemon(config.device_id)
    daemon.handlers.add(handle)
    daemon.start()
