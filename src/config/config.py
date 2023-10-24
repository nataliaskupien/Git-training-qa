import os
import json
from typing import Any

class EnvConfigProvider:
    
    @staticmethod
    def get(item_name: str) -> Any:
        value = os.getenv(item_name)
        return value

class JsonConfigProvider():

    @staticmethod
    def _readconfig(config_path):
        with open(config_path) as json_file:
            return json.load(json_file)

    @staticmethod
    def get(item_name: str) ->Any:
        value = JsonConfigProvider._readconfig("envs/dev.json")
        return value.get(item_name)

class Config:
    def __init__(self, config_providers) -> None:
        self.config_providers = config_providers
        self.config_dict = {}

        self._register("PARAMETER_JSON")
        self._register("USERNAME")

    def _register(self, item_name: str) -> None:
        for provider in self.config_providers:
            value = provider.get(item_name)
            if value is not None:
                self.config_dict[item_name] = value
                return

        raise ValueError(f"{item_name} name is missing in config providers")
    
    def __getattr__(self, item_name: str) -> Any:
        if item_name not in self.config_dict:
            raise AttributeError(f"Please register '{item_name}' var before usage")
        
        return self.config_dict[item_name]

config = Config([EnvConfigProvider,JsonConfigProvider])

print(config.__getattr__('PARAMETER_JSON'))
print(config.__getattr__('USERNAME'))