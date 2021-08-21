import os
from pathlib import Path
from shutil import copyfile
from typing import Dict, Union

import yaml
from xdg import BaseDirectory

CONFIG_FILE_NAME = 'pyg600.yaml'


class ConfigException(Exception):
    pass


class KeyConfig:
    def __init__(self, key: str, data: Dict[str, Union[str, Dict]]):
        self.key = key
        self.down = data.get('down', None)
        self.held = data.get('held', None)
        self.up = data.get('up', None)
        mod_data = data.get('mod', None)
        if mod_data:
            self.mod = KeyConfig(self.key, mod_data)
        else:
            self.mod = None

    def get_command(self, state: str, is_mod: bool):
        if is_mod:
            if self.mod:
                return self.mod.get_command(state, False)
            return None
        if state == 'down':
            return self.down
        if state == 'held':
            return self.held
        if state == 'up':
            return self.up
        return None


class Config:
    _key_configs: Dict[str, KeyConfig] = {}
    _device: str
    _last_modified: float = None

    def __init__(self, use_default=False):
        self.config_location = Config._find_config() if not use_default else Config._default_config_path()
        print(f"Using config file at {self.config_location}")

    def _load(self):
        if os.path.getmtime(self.config_location) != self._last_modified:
            with open(self.config_location, 'r') as f:
                data = yaml.safe_load(f)
            self._last_modified = os.path.getmtime(self.config_location)

            self._key_configs = {k: KeyConfig(k, v) for k, v in data.get('keys', {}).items()}
            self._device = data.get('device')

    @property
    def key_configs(self):
        self._load()
        return self._key_configs

    @property
    def device(self):
        self._load()
        return self._device

    @staticmethod
    def _find_config():
        config_base = Path(BaseDirectory.xdg_config_home)
        config_path = config_base.joinpath(CONFIG_FILE_NAME)
        if config_path.exists():
            return config_path
        return Config._create_config(config_path)

    @staticmethod
    def _create_config(config_location: Path):
        print(f"Creating default config file at {config_location}")
        copyfile(Config._default_config_path(), config_location)
        return config_location

    @staticmethod
    def _default_config_path():
        return Path(os.path.realpath(__file__)).parent.joinpath('default.yaml')
