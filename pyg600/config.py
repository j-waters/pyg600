from typing import Dict, Union
from pymacropad import Config as BaseConfig, KeyConfig

from pymacropad.daemon import KeyState

CONFIG_FILE_NAME = 'pyg600.yaml'


class ConfigException(Exception):
    pass


class ModKeyConfig(KeyConfig):
    def __init__(self, key: str, data: Dict[str, Union[str, Dict]]):
        super().__init__(key, data)
        mod_data = data.get('mod', None)
        if mod_data:
            self.mod = ModKeyConfig(self.key, mod_data)
        else:
            self.mod = None

    def get_command_with_mod(self, state: KeyState, is_mod: bool):
        if is_mod:
            if self.mod:
                return self.mod.get_command(state)
            return None
        return self.get_command(state)


class Config(BaseConfig):
    def __init__(self, use_default=False):
        super().__init__(CONFIG_FILE_NAME, use_default)

    @classmethod
    def _build_key_config(cls, key: str, data: dict) -> ModKeyConfig:
        return ModKeyConfig(key, data)


