from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class Node:
    def accept(self, visitor: "AstVisitor"):
        raise NotImplementedError()


@dataclass
class Number(Node):
    value: int

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_number(self)


@dataclass
class BinaryOperator(Enum):
    ADD = 1
    MULTIPLY = 2
    GREATER_THAN = 3
    LESS_THAN = 4
    EQUALS = 5
    SUBTRACT = 6


@dataclass
class BinaryOperation(Node):
    operator: BinaryOperator
    left: Node
    right: Node

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_binary_operation(self)


@dataclass
class Import(Node):
    value: str

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_import(self)


@dataclass
class Param(Node):
    name: str
    type: str

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_param(self)


@dataclass
class If(Node):
    condition: Node
    then_statements: List[Node]
    else_statements: Optional[List[Node]]

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_if(self)


@dataclass
class Argument(Node):
    name: str
    value: Node

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_argument(self)


@dataclass
class Function(Node):
    name: str
    is_exported: bool
    params: List[Param]
    result: Optional[str]
    body: List[Node]

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_function(self)


@dataclass
class FunctionCall(Node):
    name: str
    arguments: List[Argument]

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_function_call(self)


@dataclass
class Return(Node):
    value: Node

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_return(self)


@dataclass
class Let(Node):
    name: str
    value: Node

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_let(self)


@dataclass
class Variable(Node):
    name: str

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_variable(self)


@dataclass
class Program:
    imports: List[Import]
    functions: List[Function]

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_program(self)


class AstVisitor:
    def visit_program(self, program: Program):
        raise NotImplementedError()

    def visit_number(self, number: Number):
        raise NotImplementedError()

    def visit_variable(self, variable: Variable):
        raise NotImplementedError()

    def visit_let(self, let: Let):
        raise NotImplementedError()

    def visit_return(self, return_: Return):
        raise NotImplementedError()

    def visit_function_call(self, function_call: FunctionCall):
        raise NotImplementedError()

    def visit_function(self, function: Function):
        raise NotImplementedError()

    def visit_argument(self, argument: Argument):
        raise NotImplementedError()

    def visit_import(self, import_: Import):
        raise NotImplementedError()

    def visit_binary_operation(self, binary_operation: BinaryOperation):
        raise NotImplementedError()

    def visit_param(self, param: Param):
        raise NotImplementedError()

    def visit_if(self, if_: If):
        raise NotImplementedError()
