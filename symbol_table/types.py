from dataclasses import dataclass
from typing import Optional, List


class Type:
    def is_i32(self) -> bool:
        return False

    def is_boolean(self) -> bool:
        return False

    def is_trait(self) -> bool:
        return False

    def is_data(self) -> bool:
        return False

    def is_data_ref(self) -> bool:
        return False

    def is_void(self) -> bool:
        return False

    def is_function(self) -> bool:
        return False

    def is_placeholder(self) -> bool:
        return False


@dataclass
class Placeholder(Type):
    """
    Placeholder type which is used until the real type information is known.
    This value is used during the initial parse -> ast_generaton stage before semantic analysis occurs.

    The text represents the raw text value of the given Type information if it was present.
    """

    text: Optional[str]

    def is_placeholder(self):
        return True


@dataclass
class I32(Type):
    def is_i32(self) -> bool:
        return True


@dataclass
class Boolean(Type):
    def is_boolean(self) -> bool:
        return True


@dataclass
class Void(Type):
    def is_void(self) -> bool:
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
class TypeRef(Type):
    """
    Type ref is a reference to a data/trait definition type accessed via a string instead of a concrete type.
    This is used for 'lazy' evaluation of the type after the declarative semantic analysis has complete.
    """

    name: str

    def is_data_ref(self) -> bool:
        return True


@dataclass
class Trait(Type):
    name: str
    functions: List[Function]

    def is_trait(self) -> bool:
        return True


@dataclass
class Data(Type):
    name: str
    implements: List[TypeRef]
    fields: List[Field]
    functions: List[Function]

    def is_data(self) -> bool:
        return True
