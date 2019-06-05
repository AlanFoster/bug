from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from symbol_table.types import Type


@dataclass
class Node:
    def accept(self, visitor: "AstVisitor"):
        raise NotImplementedError()


@dataclass
class Number(Node):
    value: int

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_number(self)


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
    type: Type

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
    type: Type
    body: List[Node]

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_function(self)


@dataclass
class DataDef(Node):
    name: str
    is_exported: bool
    # TODO: Rename this to fields
    params: List[Param]
    functions: List[Function]
    type: Type

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_data_def(self)


@dataclass
class MemberAccess(Node):
    value: Node
    member: str

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_member_access(self)


@dataclass
class FunctionCall(Node):
    # TODO: This should most likely be an expression to support something like (a.b.c)()
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


# TODO: Perhaps rename to "Name"
@dataclass
class Variable(Node):
    name: str

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_variable(self)


@dataclass
class Program:
    imports: List[Import]
    data_defs: List[DataDef]
    functions: List[Function]

    def accept(self, visitor: "AstVisitor"):
        return visitor.visit_program(self)


class AstVisitor:
    @abstractmethod
    def visit_program(self, program: Program):
        raise NotImplementedError()

    @abstractmethod
    def visit_number(self, number: Number):
        raise NotImplementedError()

    @abstractmethod
    def visit_variable(self, variable: Variable):
        raise NotImplementedError()

    @abstractmethod
    def visit_let(self, let: Let):
        raise NotImplementedError()

    @abstractmethod
    def visit_return(self, return_: Return):
        raise NotImplementedError()

    @abstractmethod
    def visit_function_call(self, function_call: FunctionCall):
        raise NotImplementedError()

    @abstractmethod
    def visit_function(self, function: Function):
        raise NotImplementedError()

    @abstractmethod
    def visit_argument(self, argument: Argument):
        raise NotImplementedError()

    @abstractmethod
    def visit_import(self, import_: Import):
        raise NotImplementedError()

    @abstractmethod
    def visit_binary_operation(self, binary_operation: BinaryOperation):
        raise NotImplementedError()

    @abstractmethod
    def visit_param(self, param: Param):
        raise NotImplementedError()

    @abstractmethod
    def visit_if(self, if_: If):
        raise NotImplementedError()

    @abstractmethod
    def visit_data_def(self, data: DataDef):
        raise NotImplementedError()

    @abstractmethod
    def visit_member_access(self, member: MemberAccess):
        raise NotImplementedError()
