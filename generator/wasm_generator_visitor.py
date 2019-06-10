from typing import Optional

from symbol_table.symbol_table import EmptySymbolTable, Symbol, SymbolKind
from symbol_table import types
import compiler.ast as ast
from wasm.model import (
    Module,
    Func,
    BinaryOperation,
    Call,
    Param,
    Const,
    LocalSet,
    LocalGet,
    Local,
    Result,
    If,
    Nop,
    Return,
    Import,
    GlobalGet,
    GlobalSet,
    Store,
    Load,
)


class GeneratorException(Exception):
    """
    An unexpected error occurred during code generation.
    """


def get_binary_operator(operator):
    if operator is ast.BinaryOperator.ADD:
        return "i32.add"
    elif operator is ast.BinaryOperator.MULTIPLY:
        return "i32.mul"
    elif operator is ast.BinaryOperator.GREATER_THAN:
        return "i32.gt_s"
    elif operator is ast.BinaryOperator.LESS_THAN:
        return "i32.lt_s"
    elif operator is ast.BinaryOperator.EQUALS:
        return "i32.eq"
    elif operator is ast.BinaryOperator.SUBTRACT:
        return "i32.sub"
    elif operator is ast.BinaryOperator.AND:
        return "i32.and"
    elif operator is ast.BinaryOperator.OR:
        return "i32.or"
    else:
        raise NotImplementedError(f"Binary operator '{operator}' not implemented.")


# TODO: Add language support for type inference within the semantic analysis stage
def infer_type(variable_name: str) -> types.Type:
    if variable_name.startswith("person"):
        return types.TypeRef(name="Person")
    if variable_name.startswith("tail"):
        return types.TypeRef(name="VectorArray")
    elif variable_name.startswith("vectorArray"):
        return types.TypeRef(name="VectorArray")
    elif variable_name.startswith("vector"):
        return types.TypeRef(name="Vector")
    else:
        return types.I32()


def as_wasm_type(type_: types.Type) -> Optional[str]:
    if type_.is_data_ref():
        # If the required language type is a data ref, then we require a i32 pointer
        return "i32"
    elif type_.is_i32():
        return "i32"
    elif type_.is_boolean():
        # 32 bit integers also serve as Booleans
        return "i32"
    elif type_.is_void():
        return None
    else:
        raise TypeError(f"{type_}")


class AstVisitor(ast.AstVisitor):
    def __init__(self):
        self.symbol_table: EmptySymbolTable = EmptySymbolTable()
        self.data_name = None

    def visit_program(self, program: ast.Program):
        imports = []
        for import_ in program.imports:
            imports.append(import_.accept(self))

        self.symbol_table = self.symbol_table.enter_scope()
        data_defs = []
        for data_def in program.data_defs:
            data_defs += data_def.accept(self)

        functions = []
        for function in program.functions:
            functions.append(function.accept(self))
        self.symbol_table = self.symbol_table.exit_scope()

        instructions = []
        instructions += data_defs
        instructions += functions

        return Module(imports=imports, instructions=instructions)

    def visit_number(self, number: ast.Number):
        return Const(type="i32", val=str(number.value))

    def visit_variable(self, variable: ast.Variable):
        symbol = self.symbol_table.get(variable.name)
        return LocalGet(name=symbol.generated_name)

    def visit_let(self, let: ast.Let):
        expression = let.value.accept(self)
        symbol = Symbol(name=let.name, type=infer_type(let.name), kind=SymbolKind.LOCAL)
        self.symbol_table.add(symbol)

        return LocalSet(name=symbol.generated_name, val=expression)

    def visit_return(self, return_: ast.Return):
        return Return(expression=return_.value.accept(self) if return_.value else Nop())

    def visit_function_call(self, function_call: ast.FunctionCall):
        is_method_access = "." in function_call.name

        # Note: ast_generaton.This will need to use a real symbol table in the future
        if function_call.name == "println":
            function_name = "$output_println"
        elif self.symbol_table.has(function_call.name):
            symbol = self.symbol_table.get(function_call.name)
            if symbol.kind not in (SymbolKind.FUNC, SymbolKind.DATA):
                raise NotImplementedError(
                    f"{function_call.name} is not a function or data"
                )

            function_name = symbol.generated_name
        elif is_method_access:
            # crudely support member access for now, this should be properly
            # implemented with Call containing an expression in the future
            target, method = function_call.name.split(".")
            target_symbol = self.symbol_table.get(target)
            if target_symbol.type.is_data_ref():
                function_name = f"${target_symbol.type.name}.{method}"
            elif self.symbol_table.has(target):
                raise NotImplementedError()
        else:
            raise NotImplementedError(f"{function_call.name} not supported")
        arguments = []

        # Additionally prepend the `self` argument to this function call
        if is_method_access:
            arguments.append(LocalGet(name=target_symbol.generated_name))
        for argument in function_call.arguments:
            arguments.append(argument.accept(self))

        return Call(name=function_name, arguments=arguments)

    def visit_function(self, function: ast.Function):
        # Place the current function into the symbol table so that it can be called by
        # other functions later, or recursively if required.
        function_symbol = Symbol(
            name=function.name, type=function.type, kind=SymbolKind.FUNC
        )
        self.symbol_table.add(function_symbol)
        self.symbol_table = self.symbol_table.enter_scope()

        # Populate the required params into the symbol table before compiling the function body
        params = []
        for param in function.params:
            symbol = Symbol(name=param.name, type=param.type, kind=SymbolKind.PARAM)
            self.symbol_table.add(symbol)
            params.append(Param(type="i32", name=symbol.generated_name))
        body = []
        for statement in function.body:
            body.append(statement.accept(self))

        # After visiting the function body, any local variables will now be in the symbol table
        locals_ = []
        for symbol in self.symbol_table.locals():
            locals_.append(
                Local(type=as_wasm_type(symbol.type), name=symbol.generated_name)
            )
        self.symbol_table = self.symbol_table.exit_scope()

        assert isinstance(function.type, types.Function)
        return Func(
            # Note: The function name is the internally generated name for this module
            # Data definitions can have associated functions, in this case they will be compiled as:
            # `Vector.foo`, otherwise the normal function name will be used `foo`
            name=(
                f"${self.data_name}.{function.name}"
                if self.data_name
                else f"${function.name}"
            ),
            # Note: ast_generaton.The export name is the original function name
            export=function.name if function.is_exported else None,
            params=params,
            result=Result(type=as_wasm_type(function.type.result)),
            locals=locals_,
            instructions=body,
        )

    def visit_argument(self, argument: ast.Argument):
        # Note: In the future, these variable names will have to map to the correct argument order
        # _variable_name = argument.name
        expression = argument.value.accept(self)

        return expression

    def visit_import(self, import_: ast.Import):
        if import_.value != "System::Output":
            raise NotImplementedError(
                f"Import statement '{import_.value}' not yet supported."
            )

        return Import(
            name="$output_println",
            import_=("System::Output", "println"),
            params=[Param(type="i32", name=None)],
            result=Result(type=None),
        )

    def visit_binary_operation(self, binary_operation: ast.BinaryOperation):
        operation = get_binary_operator(binary_operation.operator)
        left = binary_operation.left.accept(self)
        right = binary_operation.right.accept(self)

        return BinaryOperation(op=operation, left=left, right=right)

    def visit_param(self, param: ast.Param):
        raise NotImplementedError()

    def visit_if(self, if_: ast.If):
        condition = if_.condition.accept(self)
        then_statements = []
        for statement in if_.then_statements:
            then_statements.append(statement.accept(self))
        else_statements = []
        if if_.else_statements:
            for statement in if_.else_statements:
                else_statements.append(statement.accept(self))

        return If(
            condition=condition,
            # TODO: ast_generaton.The result type will have to be inferred correctly
            result=Result(type=None),
            then_statements=then_statements,
            else_statements=else_statements if else_statements else None,
        )

    def visit_data_def(self, data: ast.DataDef):
        self.data_name = data.name

        # Update the current symbol table with the current data class details
        self.symbol_table.add(
            Symbol(name=data.name, type=data.type, kind=SymbolKind.DATA)
        )

        # Specify all known functions

        malloc_self = GlobalSet(
            name="$self_pointer",
            val=Call(name="$malloc", arguments=[Const(type="i32", val="2")]),
        )

        params = []
        param_assignments = []
        for index, param in enumerate(data.params):
            assert isinstance(param.type, types.Field)
            params.append(
                Param(type=as_wasm_type(param.type.type), name=f"${param.name}")
            )
            param_assignments.append(
                Store(
                    type=as_wasm_type(param.type.type),
                    location=(
                        BinaryOperation(
                            op="i32.add",
                            left=GlobalGet(name="$self_pointer"),
                            right=Const(type="i32", val=str(4 * index)),
                        )
                    ),
                    val=LocalGet(name=f"${param.name}"),
                )
            )

        return_self = GlobalGet(name="$self_pointer")

        instructions = []
        instructions += [malloc_self]
        instructions += param_assignments
        instructions += [return_self]

        constructor = Func(
            name=f"${data.name}.new",
            export=None,
            params=params,
            result=Result(type="i32"),
            locals=[],
            instructions=instructions,
        )

        # Enter a new scope when creating function definitions, and assign the data definitions fields
        # so that they can be accessed later within the function bodies
        self.symbol_table = self.symbol_table.enter_scope()
        for index, param in enumerate(data.params):
            self.symbol_table.add(
                Symbol(
                    name=param.name,
                    type=param.type,
                    kind=SymbolKind.DATA_FIELD,
                    field_number=index,
                )
            )

        data_funcs = []
        for func in data.functions:
            data_funcs.append(func.accept(self))
        self.data_name = None
        self.symbol_table = self.symbol_table.exit_scope()

        return [constructor] + data_funcs

    # TODO: Only works on param access currently
    def visit_member_access(self, member: ast.MemberAccess):
        if not isinstance(member.value, ast.Variable):
            raise TypeError(f"No support added for {member} yet.")

        left = member.value.name
        right = member.member

        left_param_symbol = self.symbol_table.get(left)
        left_param_type = left_param_symbol.type
        assert isinstance(left_param_type, types.Param)

        left_type_ref = left_param_type.type
        assert isinstance(left_type_ref, types.TypeRef)
        left_type = self.symbol_table.get(left_type_ref.name).type
        assert isinstance(left_type, types.Data)
        right_field_index = None
        for index, field in enumerate(left_type.fields):
            if field.name == right:
                right_field_index = index
        if right_field_index is None:
            raise GeneratorException(
                f"Unable to find find field_index for '{left}.{right}'"
            )

        # Load from memory the required field by calculating its field number relative to its self pointer
        # field = self_pointer + (field_number * 4)
        return Load(
            type="i32",
            location=(
                BinaryOperation(
                    op="i32.add",
                    left=LocalGet(name=left_param_symbol.generated_name),
                    right=(
                        BinaryOperation(
                            op="i32.mul",
                            left=Const(type="i32", val=str(right_field_index)),
                            right=Const(type="i32", val="4"),
                        )
                    ),
                )
            ),
        )
