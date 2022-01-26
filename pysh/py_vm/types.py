from __future__ import annotations

from typing import Optional, Any, Tuple, cast
from enum import Enum

class Primatives(Enum):
    Unknown = -1
    String = 0
    Int = 1
    Float = 2
    Bool = 3
    Array = 4
    Dict = 5
    Function = 6

    @classmethod
    def getType(cls, value) -> Primatives:
        if isinstance(value, str):
            return cls.String
        if isinstance(value, bool):
            return cls.Bool
        if isinstance(value, int):
            return cls.Int
        if isinstance(value, float):
            return cls.Float
        if callable(value):
            return cls.Function
        return cls.Unknown


    def __eq__(self, o: Any):
      return type(self) == type(o) and self.value == o.value

    def __str__(self):
      return f'{self.name}'

DATUM_PRIMATIVES = [Primatives.String, Primatives.Int, Primatives.Float, Primatives.Bool, Primatives.Unknown]
DATUM_COLLECTIONS = [Primatives.Array, Primatives.Dict, Primatives.Function]

class UserType:
    def __init__(self, primary_type: Primatives, secondary_type: Optional[Primatives] = None):
        self.primary_type = primary_type
        if self.primary_type in [Primatives.Dict, Primatives.Array]:
            if secondary_type in [Primatives.Array, Primatives.Dict, None]:
                raise ValueError(
                    f"Incomplete secondary type {secondary_type} for primary type {primary_type}")
            else:
                self.secondary_type = secondary_type
        else:
            if secondary_type != None:
                raise ValueError(
                    f"Incomplete secondary type {secondary_type} for primary type {primary_type}")
            self.secondary_type = secondary_type

    @classmethod
    def factory(cls, value: Any) -> UserType:
        if isinstance(value, list):
            if len(value) == 0:
                return UserType(Primatives.Array, Primatives.Unknown)
            else:
                return UserType(Primatives.Array, Primatives.getType(value[0]))
        if isinstance(value, dict):
            if len(value) == 0:
                return UserType(Primatives.Dict, Primatives.Unknown)
            for k, v in value.items():
                return UserType(Primatives.Dict, Primatives.getType(k))
        return UserType(Primatives.getType(value))

    def __eq__(self, o: object) -> bool:
        return type(o) == UserType and self.primary_type == o.primary_type and self.secondary_type == o.secondary_type

    def __str__(self):
        if self.is_collection():
            return f'{self.primary_type}[{self.secondary_type}]'
        return f'{self.primary_type}'

    def __repr__(self):
        if self.is_collection():
            return f'{self.primary_type}[{self.secondary_type}]'
        return f'{self.primary_type}'

    def as_tuple(self) -> Tuple[Primatives, Optional[Primatives]]:
        return (self.primary_type, self.secondary_type)

    def convertable(self, other: UserType) -> bool:
        s_a, s_b = self.as_tuple()
        o_a, o_b = other.as_tuple()
        if s_a in DATUM_PRIMATIVES and o_a in DATUM_PRIMATIVES:
            return True
        if s_a in DATUM_COLLECTIONS:
            return s_a == o_a
        return False

    def is_collection(self) -> bool:
        return self.primary_type in DATUM_COLLECTIONS
        



class UserValue:
    """
    Represents a value specified by a user in a
    language-independent way.

    This is useful because it allows for easy conversion
    back and forth between a bash-compatible value
    and a python-compatible value
    """

    def __init__(self, value, value_type: UserType):
        self.value = value
        self.value_type = value_type

    def convert_type(self, other_type: UserType):
        if self.value_type.convertable(other_type):
            if self.value_type.is_collection():
                return self._convert_collection(other_type)
            return UserValue(self._convert_value(other_type), other_type)
        raise ValueError(f'Cannot convert {self} to type {other_type}')

    @property
    def type(self):
        return self.value_type

    def _convert_value(self, other_type: UserType):
        if other_type.primary_type == Primatives.String:
            return str(self.value)
        if other_type.primary_type == Primatives.Float:
            return float(self.value)
        if other_type.primary_type == Primatives.Int:
            return int(self.value)
        if other_type.primary_type == Primatives.Bool:
            if self.value == '0' or self.value == 0 or self.value == 0.0:
                return False
            return bool(self.value)

    def _convert_collection(self, other_type: UserType):
        element_type = UserType(cast(Primatives, self.value_type.secondary_type))
        dest_type = UserType(cast(Primatives, other_type.secondary_type))
        if other_type.primary_type == Primatives.Array:
            return UserValue([
                UserValue(elem, element_type).convert_type(dest_type).value
                for elem in self.value
            ], other_type)
        else: # Must be a dict 
            return UserValue({
                k: UserValue(v, element_type).convert_type(dest_type).value
                for k, v in self.value.items()
            }, other_type)

    def __str__(self):
        return f'<{self.value}: {self.value_type}>'
        
