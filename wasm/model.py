from abc import abstractmethod
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
        return visitor.visit_module(self)


@dataclass
class Param:
    type: str
    name: str = None

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_param(self)


@dataclass
class Local:
    type: str
    name: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_local(self)


@dataclass
class Result:
    type: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_result(self)


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
    import_: Any = None
    params: List[Param] = None
    result: Result = None
    locals: List[Local] = None
    instructions: List[Instruction] = None

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_func(self)


@dataclass
class BinaryOperation(Instruction):
    op: str
    left: Instruction
    right: Instruction

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_binary_operation(self)


@dataclass
class GetLocal(Instruction):
    name: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_get_local(self)


@dataclass
class SetLocal(Instruction):
    name: str
    val: Instruction

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_set_local(self)


@dataclass
class Const(Instruction):
    type: str
    val: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_const(self)


@dataclass
class Call(Instruction):
    """
    `call` is used for static calls, i.e. where the function name is known ahead of time.
    `call_indirect` can be used when the function to call is on the stack.
    """

    name: str
    arguments: List[Instruction]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_call(self)


class WasmVisitor:
    @abstractmethod
    def visit_module(self, module: Module):
        raise NotImplementedError()

    @abstractmethod
    def visit_param(self, param: Param):
        raise NotImplementedError()

    @abstractmethod
    def visit_result(self, result: Result):
        raise NotImplementedError()

    @abstractmethod
    def visit_local(self, param: Local):
        raise NotImplementedError()

    @abstractmethod
    def visit_get_local(self, param: GetLocal):
        raise NotImplementedError()

    @abstractmethod
    def visit_set_local(self, local: SetLocal):
        raise NotImplementedError()

    @abstractmethod
    def visit_func(self, func: Func):
        raise NotImplementedError()

    @abstractmethod
    def visit_binary_operation(self, binary_operation: BinaryOperation):
        raise NotImplementedError()

    @abstractmethod
    def visit_const(self, const: Const):
        raise NotImplementedError()

    @abstractmethod
    def visit_call(self, call: Call):
        raise NotImplementedError()
