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
    imports: List["Import"]
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
class Import(Instruction):
    name: Optional[str]
    import_: Optional[Any]
    params: List[Param]
    result: Optional[Result]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_import(self)


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

    name: Optional[str]
    export: Optional[str]
    params: List[Param]
    locals: List[Local]
    instructions: List[Instruction]
    result: Optional[Result]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_func(self)


@dataclass
class BinaryOperation(Instruction):
    # TODO: Rename this to operator
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


@dataclass
class If(Instruction):
    result: Optional[Result]
    condition: Instruction
    then_statements: List[Instruction]
    else_statements: Optional[List[Instruction]]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_if(self)


@dataclass
class Return(Instruction):
    expression: Optional[Instruction]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_return(self)


@dataclass
class Nop(Instruction):
    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_nop(self)


@dataclass
class Global(Instruction):
    name: str
    type: str
    value: Instruction

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_global(self)


@dataclass
class GetGlobal(Instruction):
    name: str

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_get_global(self)


@dataclass
class SetGlobal(Instruction):
    name: str
    val: Instruction

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_set_global(self)


@dataclass
class Store(Instruction):
    type: str
    location: Instruction
    val: Instruction

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_store(self)


@dataclass
class Load(Instruction):
    type: str
    location: Instruction

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_load(self)


@dataclass
class Memory(Instruction):
    size: int
    export: Optional[str]

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_memory(self)


@dataclass
class Drop:
    """
     The drop operator throws away a single operand
    """

    def accept(self, visitor: "WasmVisitor"):
        return visitor.visit_drop(self)


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
    def visit_import(self, import_: Import):
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

    @abstractmethod
    def visit_if(self, if_: If):
        raise NotImplementedError()

    @abstractmethod
    def visit_drop(self, drop: Drop):
        raise NotImplementedError()

    @abstractmethod
    def visit_return(self, return_: Return):
        raise NotImplementedError()

    @abstractmethod
    def visit_nop(self, return_: Return):
        raise NotImplementedError()

    @abstractmethod
    def visit_global(self, global_: Global):
        raise NotImplementedError()

    @abstractmethod
    def visit_get_global(self, get_global: GetGlobal):
        raise NotImplementedError()

    @abstractmethod
    def visit_set_global(self, set_global: SetGlobal):
        raise NotImplementedError()

    @abstractmethod
    def visit_memory(self, memory: Memory):
        raise NotImplementedError()

    @abstractmethod
    def visit_store(self, store: Store):
        raise NotImplementedError()

    @abstractmethod
    def visit_load(self, load: Load):
        raise NotImplementedError()
