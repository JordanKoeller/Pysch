import os
from typing import Dict

from .types import UserValue


class PythonSession:

    def __init__(self):
        self._user_variables: Dict[str, UserValue] = {}

    def add_variable(self, key: str, value: UserValue, override_type: bool = None):
        if key in self._user_variables and not override_type:
            self._user_variables[key] = value.convert_type(self._user_variables[key].type)
        else:
            self._user_variables[key] = value
    
    
        

