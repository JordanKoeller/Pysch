import os
from typing import Dict, Any
import builtins

from .types import UserType, UserValue


class PyVm:

    def __init__(self):
        self._user_variables: Dict[str, Any] = {}
        self._user_variable_types: Dict[str, UserType] = {}

    def add_variable(self, key: str, valueType: UserValue, override_type: bool = None):
        if key in self._user_variables and not override_type:
            self._user_variables[key] = valueType.convert_type(self._user_variable_types[key]).value 
        else:
            self._user_variables[key] = valueType.value
            self._user_variable_types[key] = valueType.type
    
    def run_py_command(self, command: str):
        # scope = {k: v.value for k, v in self._user_variables.items()}
        exec(command, builtins.__dict__, self._user_variables)
    
        

