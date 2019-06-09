"""
Semantic analysis is currently performed in two phases:

- Declarative Analysis
- Statement/Expression Analysis

Declarative Analysis - This visitor collects the type information about the currently known data classes,
their corresponding functions, and and remaining functions.

This is performed as a first pass to ensure that that all functions are known about before
semantic analysis is applied to statements/expressions to ensure that forward references are allowed
to types that are defined later in the file - such as additional data classes or functions.
"""
from symbol_table import types
from symbol_table.symbol_table import EmptySymbolTable, Symbol, SymbolKind, SymbolTable
import compiler.ast as ast


def as_language_type(type_: types.Type, symbol_table: SymbolTable) -> types.Type:
    assert isinstance(type_, types.Placeholder)
    text = type_.text

    if text == "i32":
        return types.I32()
    if text == "void":
        return types.Void()
    if text == "boolean":
        return types.Boolean()
    if symbol_table.has(text):
        symbol = symbol_table.get(text)
        assert symbol.type.is_data() or symbol.type.is_trait()
        return types.TypeRef(name=text)
    else:
        raise TypeError(f"Type not supported: {type_}")


class DeclarationAnalysisVisitor(ast.AstVisitor):
    def __init__(self):
        self.symbol_table: EmptySymbolTable = EmptySymbolTable()
        self.data_name = None

    def visit_program(self, program: ast.Program):
        for import_ in program.imports:
            import_.accept(self)

        self.symbol_table = self.symbol_table.enter_scope()
        for trait in program.traits:
            trait.accept(self)
        for data_def in program.data_defs:
            data_def.accept(self)
        for function in program.functions:
            function.accept(self)
        self.symbol_table = self.symbol_table.exit_scope()
        return program

    def visit_number(self, number: ast.Number):
        raise NotImplementedError()

    def visit_variable(self, variable: ast.Variable):
        raise NotImplementedError()

    def visit_let(self, let: ast.Let):
        raise NotImplementedError()

    def visit_return(self, return_: ast.Return):
        raise NotImplementedError()

    def visit_function_call(self, function_call: ast.FunctionCall):
        raise NotImplementedError()

    def visit_function(self, function: ast.Function):
        """
        Visit the function definition, populating the return and param type information.
        During this stage the function body is skipped, as it may depend on types defined
        later within the file
        """

        param_types = []
        for param in function.params:
            param.type = types.Param(
                name=param.name, type=as_language_type(param.type, self.symbol_table)
            )
            param_types.append(param.type)

        function.type = types.Function(
            name=function.name,
            result=as_language_type(function.type, self.symbol_table),
            params=param_types,
        )
        function_symbol = Symbol(
            name=function.name, type=function.type, kind=SymbolKind.FUNC
        )
        self.symbol_table.add(function_symbol)
        return function

    def visit_argument(self, argument: ast.Argument):
        argument.value.accept(self)
        return argument

    def visit_import(self, import_: ast.Import):
        return import_

    def visit_binary_operation(self, binary_operation: ast.BinaryOperation):
        raise NotImplementedError()

    def visit_param(self, param: ast.Param):
        raise NotImplementedError()

    def visit_if(self, if_: ast.If):
        raise NotImplementedError()

    def visit_trait(self, trait: ast.Trait):
        trait_type = types.Trait(name=trait.name, functions=[])
        trait.type = trait_type
        self.symbol_table.add(
            Symbol(name=trait.name, type=trait_type, kind=SymbolKind.TRAIT)
        )

        self.symbol_table = self.symbol_table.enter_scope()
        for function in trait.functions:
            function.accept(self)
        self.symbol_table = self.symbol_table.exit_scope()

        return trait

    def visit_data_def(self, data: ast.DataDef):
        implements = []
        for implement in data.implements:
            implements.append(types.TypeRef(name=implement))
        data_def_type = types.Data(
            name=data.name, implements=implements, fields=[], functions=[]
        )
        data.type = data_def_type
        self.symbol_table.add(
            Symbol(name=data.name, type=data_def_type, kind=SymbolKind.DATA)
        )

        for field in data.params:
            field.type = types.Field(
                name=field.name, type=as_language_type(field.type, self.symbol_table)
            )
            data_def_type.fields.append(field.type)

        self.symbol_table = self.symbol_table.enter_scope()
        for function in data.functions:
            function.accept(self)
        self.symbol_table = self.symbol_table.exit_scope()

        return data

    def visit_member_access(self, member: ast.MemberAccess):
        raise NotImplementedError()
