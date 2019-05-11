import antlr4
from compiler.ast import (
    Program,
    If,
    Import,
    Function,
    FunctionCall,
    Argument,
    BinaryOperation,
    BinaryOperator,
    Number,
    Let,
    Variable,
    Param,
    Return,
    DataDef,
    MemberAccess,
)
from compiler import compiler


def get_ast(source: str) -> Program:
    input_stream = antlr4.InputStream(source)
    parse_tree = compiler.get_parse_tree(input_stream)
    return compiler.get_ast(parse_tree)


def test_empty_program():
    source = ""
    result = get_ast(source)

    assert result == Program(imports=[], data_defs=[], functions=[])


def test_simple_expression():
    source = """
        import System::Output;

        export function Main(): void {
            println(value=1 + 2 * 3);
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[
                    FunctionCall(
                        name="println",
                        arguments=[
                            Argument(
                                name="value",
                                value=BinaryOperation(
                                    operator=BinaryOperator.ADD,
                                    left=Number(value=1),
                                    right=BinaryOperation(
                                        operator=BinaryOperator.MULTIPLY,
                                        left=Number(value=2),
                                        right=Number(value=3),
                                    ),
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )


def test_simple_assignment():
    source = """
        import System::Output;

        export function Main(): void {
            let a = 5;
            let b = 10;
            println(value=a + b);
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[
                    Let(name="a", value=Number(5)),
                    Let(name="b", value=Number(10)),
                    FunctionCall(
                        name="println",
                        arguments=[
                            Argument(
                                name="value",
                                value=BinaryOperation(
                                    operator=BinaryOperator.ADD,
                                    left=Variable(name="a"),
                                    right=Variable(name="b"),
                                ),
                            )
                        ],
                    ),
                ],
            )
        ],
    )


def test_function_call_with_no_arguments():
    source = """
        import System::Output;

        function sayNumber(): void {
            println(value=1337);
        }

        export function Main(): void {
            sayNumber();
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="sayNumber",
                is_exported=False,
                params=[],
                result=None,
                body=[
                    FunctionCall(
                        name="println",
                        arguments=[Argument(name="value", value=Number(1337))],
                    )
                ],
            ),
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[FunctionCall(name="sayNumber", arguments=[])],
            ),
        ],
    )


def test_function_call_with_arguments():
    source = """
        import System::Output;

        function add(x: i32, y: i32): i32 {
            x + y;
        }

        export function Main(): void {
            println(value=add(a=5, b=15));
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="add",
                is_exported=False,
                params=[Param(name="x", type="i32"), Param(name="y", type="i32")],
                result="i32",
                body=[
                    BinaryOperation(
                        operator=BinaryOperator.ADD,
                        left=Variable("x"),
                        right=Variable("y"),
                    )
                ],
            ),
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[
                    FunctionCall(
                        name="println",
                        arguments=[
                            Argument(
                                name="value",
                                value=(
                                    FunctionCall(
                                        name="add",
                                        arguments=[
                                            Argument(name="a", value=Number(value=5)),
                                            Argument(name="b", value=Number(value=15)),
                                        ],
                                    )
                                ),
                            )
                        ],
                    )
                ],
            ),
        ],
    )


def test_if_statement():
    source = """
        import System::Output;

        export function Main(): void {
            if (5 > 10) {
                println(value=1);
            }
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[
                    If(
                        condition=BinaryOperation(
                            operator=BinaryOperator.GREATER_THAN,
                            left=Number(5),
                            right=Number(10),
                        ),
                        then_statements=[
                            FunctionCall(
                                name="println",
                                arguments=[Argument(name="value", value=(Number(1)))],
                            )
                        ],
                        else_statements=None,
                    )
                ],
            )
        ],
    )


#
def test_if_else_statement():
    source = """
        import System::Output;

        export function Main(): void {
            if (5 < 10) {
                println(value=1);
            } else {
                println(value=0);
            }
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[
                    If(
                        condition=BinaryOperation(
                            operator=BinaryOperator.GREATER_THAN,
                            left=Number(5),
                            right=Number(10),
                        ),
                        then_statements=[
                            FunctionCall(
                                name="println",
                                arguments=[Argument(name="value", value=(Number(1)))],
                            )
                        ],
                        else_statements=[
                            FunctionCall(
                                name="println",
                                arguments=[Argument(name="value", value=(Number(0)))],
                            )
                        ],
                    )
                ],
            )
        ],
    )


def test_factorial():
    # TODO: The precedence in this example is wrong. Additional parentheses provided for now.
    source = """
        import System::Output;

        function factorial(n: i32): i32 {
            if (n == 1) {
                return 1;
            } else {
                return n * (factorial(n=n-1));
            }
        }

        export function Main(): void {
            println(value=factorial(n=5));
        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[],
        functions=[
            Function(
                name="factorial",
                is_exported=False,
                params=[Param(name="n", type="i32")],
                result="i32",
                body=[
                    If(
                        condition=BinaryOperation(
                            operator=BinaryOperator.EQUALS,
                            left=Variable("n"),
                            right=Number(1),
                        ),
                        then_statements=[Return(value=Number(value=1))],
                        else_statements=[
                            Return(
                                value=BinaryOperation(
                                    operator=BinaryOperator.MULTIPLY,
                                    left=Variable(name="n"),
                                    right=FunctionCall(
                                        name="factorial",
                                        arguments=[
                                            Argument(
                                                name="n",
                                                value=BinaryOperation(
                                                    operator=BinaryOperator.SUBTRACT,
                                                    left=Variable(name="n"),
                                                    right=Number(value=1),
                                                ),
                                            )
                                        ],
                                    ),
                                )
                            )
                        ],
                    )
                ],
            ),
            Function(
                name="Main",
                is_exported=True,
                params=[],
                result=None,
                body=[
                    FunctionCall(
                        name="println",
                        arguments=[
                            Argument(
                                name="value",
                                value=FunctionCall(
                                    name="factorial",
                                    arguments=[Argument(name="n", value=(Number(5)))],
                                ),
                            )
                        ],
                    )
                ],
            ),
        ],
    )


def test_data_vector():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32);

        export function Main(): void {

        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[
            DataDef(
                name="Vector",
                is_exported=True,
                params=[Param(name="x", type="i32"), Param(name="y", type="i32")],
                functions=[],
            )
        ],
        functions=[
            Function(name="Main", is_exported=True, params=[], result=None, body=[])
        ],
    )


def test_data_vector_with_simple_function():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function length(): i32 {
                42;
            }
        }

        export function Main(): void {

        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[
            DataDef(
                name="Vector",
                is_exported=True,
                params=[Param(name="x", type="i32"), Param(name="y", type="i32")],
                functions=[
                    Function(
                        name="length",
                        is_exported=False,
                        params=[],
                        result="i32",
                        body=[Number(value=42)],
                    )
                ],
            )
        ],
        functions=[
            Function(name="Main", is_exported=True, params=[], result=None, body=[])
        ],
    )


def test_data_vector_with_complex_function():
    # TODO: The precedence in this example is wrong. Additional parentheses provided for now.
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function add(self: Vector, other: Vector): Vector {
                Vector(x = (self.x) + (other.x), y = (self.y) + (other.y));
            }
        }

        export function Main(): void {

        }
     """
    result = get_ast(source)

    assert result == Program(
        imports=[Import(value="System::Output")],
        data_defs=[
            DataDef(
                name="Vector",
                is_exported=True,
                params=[Param(name="x", type="i32"), Param(name="y", type="i32")],
                functions=[
                    Function(
                        name="add",
                        is_exported=False,
                        params=[
                            Param(name="self", type="Vector"),
                            Param(name="other", type="Vector"),
                        ],
                        result="Vector",
                        body=[
                            FunctionCall(
                                name="Vector",
                                arguments=[
                                    Argument(
                                        name="x",
                                        value=BinaryOperation(
                                            operator=BinaryOperator.ADD,
                                            left=MemberAccess(
                                                value=Variable("self"), member="x"
                                            ),
                                            right=MemberAccess(
                                                value=Variable("other"), member="x"
                                            ),
                                        ),
                                    ),
                                    Argument(
                                        name="y",
                                        value=BinaryOperation(
                                            operator=BinaryOperator.ADD,
                                            left=MemberAccess(
                                                value=Variable("self"), member="y"
                                            ),
                                            right=MemberAccess(
                                                value=Variable("other"), member="y"
                                            ),
                                        ),
                                    ),
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
        functions=[
            Function(name="Main", is_exported=True, params=[], result=None, body=[])
        ],
    )
