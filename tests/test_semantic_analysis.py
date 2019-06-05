import antlr4
from prettyprinter import pprint

from compiler import compiler
from tests.helpers.wasm import assert_equal_programs
from compiler import ast
from symbol_table import types


def get_semantic_analysis(source: str) -> ast.Program:
    input_stream = antlr4.InputStream(source)
    parse_tree = compiler.get_parse_tree(input_stream)
    return compiler.get_semantic_analysis(compiler.get_ast(parse_tree))


def test_simple_expression():
    source = """
        export function Main(): void {
            let a = 1 + 2 * 3;
        }
     """
    result = get_semantic_analysis(source)

    assert_equal_programs(
        result,
        ast.Program(
            imports=[],
            data_defs=[],
            functions=[
                ast.Function(
                    name="Main",
                    is_exported=True,
                    params=[],
                    type=types.Function(name="Main", params=[], result=types.Void()),
                    body=[
                        ast.Let(
                            name="a",
                            value=ast.BinaryOperation(
                                operator=ast.BinaryOperator.ADD,
                                left=ast.Number(value=1),
                                right=ast.BinaryOperation(
                                    operator=ast.BinaryOperator.MULTIPLY,
                                    left=ast.Number(value=2),
                                    right=ast.Number(value=3),
                                ),
                            ),
                        )
                    ],
                )
            ],
        ),
    )


def test_data_vector_with_complex_function():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function add(self: Vector, other: Vector): Vector {
                Vector(x = self.x + other.x, y = self.y + other.y);
            }
        }

        export function Main(): void {

        }
     """
    result = get_semantic_analysis(source)

    pprint(result)

    assert_equal_programs(
        result,
        ast.Program(
            imports=[ast.Import(value="System::Output")],
            data_defs=[
                ast.DataDef(
                    name="Vector",
                    is_exported=True,
                    params=[
                        ast.Param(
                            name="x", type=types.Field(name="x", type=types.I32())
                        ),
                        ast.Param(
                            name="y", type=types.Field(name="y", type=types.I32())
                        ),
                    ],
                    functions=[
                        ast.Function(
                            name="add",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.DataRef(name="Vector")
                                    ),
                                ),
                                ast.Param(
                                    name="other",
                                    type=types.Param(
                                        name="other", type=types.DataRef(name="Vector")
                                    ),
                                ),
                            ],
                            type=types.Function(
                                name="add",
                                params=[
                                    types.Param(
                                        name="self", type=types.DataRef(name="Vector")
                                    ),
                                    types.Param(
                                        name="other", type=types.DataRef(name="Vector")
                                    ),
                                ],
                                result=types.DataRef(name="Vector"),
                            ),
                            body=[
                                ast.FunctionCall(
                                    name="Vector",
                                    arguments=[
                                        ast.Argument(
                                            name="x",
                                            value=ast.BinaryOperation(
                                                operator=ast.BinaryOperator.ADD,
                                                left=ast.MemberAccess(
                                                    value=ast.Variable(name="self"),
                                                    member="x",
                                                ),
                                                right=ast.MemberAccess(
                                                    value=ast.Variable(name="other"),
                                                    member="x",
                                                ),
                                            ),
                                        ),
                                        ast.Argument(
                                            name="y",
                                            value=ast.BinaryOperation(
                                                operator=ast.BinaryOperator.ADD,
                                                left=ast.MemberAccess(
                                                    value=ast.Variable(name="self"),
                                                    member="y",
                                                ),
                                                right=ast.MemberAccess(
                                                    value=ast.Variable(name="other"),
                                                    member="y",
                                                ),
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                    type=types.Data(
                        name="Vector",
                        fields=[
                            types.Field(name="x", type=types.I32()),
                            types.Field(name="y", type=types.I32()),
                        ],
                        functions=[],
                    ),
                )
            ],
            functions=[
                ast.Function(
                    name="Main",
                    is_exported=True,
                    params=[],
                    type=types.Function(name="Main", params=[], result=types.Void()),
                    body=[],
                )
            ],
        ),
    )
