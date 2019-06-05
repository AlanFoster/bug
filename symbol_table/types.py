from dataclasses import dataclass
from typing import Optional, List


class Type:
    def is_i32(self):
        return False

    def is_data(self):
        return False

    def is_data_ref(self):
        return False

    def is_void(self):
        return False

    def is_function(self):
        return False

    def is_placeholder(self):
        return False


@dataclass
class Placeholder(Type):
    """
    Placeholder type which is used until the real type information is known.
    This value is used during the initial parse -> ast stage before semantic analysis occurs.

    The text represents the raw text value of the given Type information if it was present.
    """

    text: Optional[str]

    def is_placeholder(self):
        return True


@dataclass
class I32(Type):
    def is_i32(self):
        return True


@dataclass
class Void(Type):
    def is_void(self):
        return True


@dataclass
class Param(Type):
    name: str
    type: Type


@dataclass
class Function(Type):
    name: str
    params: List[Param]
    result: Type


@dataclass
class Field(Type):
    name: str
    type: Type


@dataclass
class Data(Type):
    name: str
    fields: List[Field]
    functions: List[Function]

    def is_data(self):
        return True


@dataclass
class DataRef(Type):
    """
    Data ref is a reference to a data definition type accessed via a string instead of a concrete type.
    """

    name: str

    def is_data_ref(self):
        return True
