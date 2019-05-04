from typing import List, Optional, Any
from dataclasses import dataclass


# Models extracted from the web assembly spec:
#   https://github.com/WebAssembly/spec/tree/6281d0d386845cc7b1aa3a2150b0203307909861/interpreter#s-expression-syntax


@dataclass
class Instruction:
    def accept(self, visitor: "WasmVisitor"):
        raise NotImplementedError()


@dataclass
class Module:
    instructions: List[Instruction]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visitModule(self)


@dataclass
class Param:
    type: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visitParam(self)


@dataclass
class Func(Instruction):
    """
    ( func <signature> <locals> <body> )
    ( func (param i32) (param i32) (result f64) (local f64) (local i32) ... )
    Absence of result indicates no return value

    Reference locals with `get_local 0`, `get_local 1`, or more readable:
    ( func (param $p1 i32) (param $p2 i32) (result f64) (local $a f64) (local $b i32) ... )
    Reference locals with `get_local $p1`, `get_local $a`
    """

    name: Optional[str] = None
    export: Optional[str] = None
    # import_: Optional[(str, str)] = None
    import_: Any = None
    params: List[Param] = None
    instructions: List[Instruction] = None

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visitFunc(self)


@dataclass
class Operation(Instruction):
    def accept(self, visitor: "WasmVisitor"):
        raise NotImplementedError()


@dataclass
class BinaryOperation(Operation):
    op: str
    left: Operation
    right: Operation

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visitBinaryOperation(self)


@dataclass
class Const(Operation):
    val_type: str
    val: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visitConst(self)


@dataclass
class Call(Operation):
    """
    `call` is used for static calls, i.e. where the function name is known ahead of time.
    `call_indirect` can be used when the function to call is on the stack.
    """

    var: str
    arguments: List[Instruction]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visitCall(self)


class WasmVisitor:
    def visitModule(self, module: Module):
        pass

    def visitParam(self, param: Param):
        pass

    def visitFunc(self, func: Func):
        pass

    def visitBinaryOperation(self, binary_operation: BinaryOperation):
        pass

    def visitConst(self, const: Const):
        pass

    def visitCall(self, call: Call):
        pass
