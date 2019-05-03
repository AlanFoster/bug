from typing import List, Optional, Any
from dataclasses import dataclass

# Models extracted from the web assembly spec:
#   https://github.com/WebAssembly/spec/tree/6281d0d386845cc7b1aa3a2150b0203307909861/interpreter#s-expression-syntax


@dataclass
class Instruction:
    pass


@dataclass
class Module:
    instructions: List[Instruction]


@dataclass
class Param:
    type: str


@dataclass
class Func(Instruction):
    name: Optional[str] = None
    export: Optional[str] = None
    # import_: Optional[(str, str)] = None
    import_: Any = None
    params: List[Param] = None
    instructions: List[Instruction] = None


@dataclass
class Operation(Instruction):
    pass


@dataclass
class BinaryOperation(Operation):
    op: str
    left: List[Operation]
    right: List[Operation]


@dataclass
class Const(Operation):
    val_type: str
    val: str


@dataclass
class Call(Operation):
    var: str
