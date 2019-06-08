import antlr4

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
            traits=[],
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

    assert_equal_programs(
        result,
        ast.Program(
            imports=[ast.Import(value="System::Output")],
            traits=[],
            data_defs=[
                ast.DataDef(
                    name="Vector",
                    implements=[],
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
                                        name="self", type=types.TypeRef(name="Vector")
                                    ),
                                ),
                                ast.Param(
                                    name="other",
                                    type=types.Param(
                                        name="other", type=types.TypeRef(name="Vector")
                                    ),
                                ),
                            ],
                            type=types.Function(
                                name="add",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="Vector")
                                    ),
                                    types.Param(
                                        name="other", type=types.TypeRef(name="Vector")
                                    ),
                                ],
                                result=types.TypeRef(name="Vector"),
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
                        implements=[],
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

    assert_equal_programs(
        result,
        ast.Program(
            imports=[ast.Import(value="System::Output")],
            traits=[],
            data_defs=[
                ast.DataDef(
                    name="Vector",
                    implements=[],
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
                                        name="self", type=types.TypeRef(name="Vector")
                                    ),
                                ),
                                ast.Param(
                                    name="other",
                                    type=types.Param(
                                        name="other", type=types.TypeRef(name="Vector")
                                    ),
                                ),
                            ],
                            type=types.Function(
                                name="add",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="Vector")
                                    ),
                                    types.Param(
                                        name="other", type=types.TypeRef(name="Vector")
                                    ),
                                ],
                                result=types.TypeRef(name="Vector"),
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
                        implements=[],
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


def test_trait_with_no_functions():
    source = """
        trait List {

        }
     """
    result = get_semantic_analysis(source)

    assert_equal_programs(
        result,
        ast.Program(
            imports=[],
            traits=[
                ast.Trait(
                    name="List",
                    is_exported=False,
                    type=types.Trait(name="List", functions=[]),
                    functions=[],
                )
            ],
            data_defs=[],
            functions=[],
        ),
    )


def test_trait_with_multiple_implementations():
    source = """
        trait List {
            function length(self: List): i32;
            function sum(self: List): i32;
        }

        data EmptyList() implements List {
            function length(self: List): i32 {
                0;
            }

            function sum(self: List): i32 {
                0;
            }
        }

        data Cons(head: i32, tail: List) implements List {
            function length(self: List): i32 {
                1 + self.tail.length();
            }

            function sum(self: List): i32 {
                self.head + self.tail.sum();
            }
        }
     """
    result = get_semantic_analysis(source)

    assert_equal_programs(
        result,
        ast.Program(
            imports=[],
            traits=[
                ast.Trait(
                    name="List",
                    is_exported=False,
                    functions=[
                        ast.Function(
                            name="length",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    ),
                                )
                            ],
                            type=types.Function(
                                name="length",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    )
                                ],
                                result=types.I32(),
                            ),
                            body=None,
                        ),
                        ast.Function(
                            name="sum",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    ),
                                )
                            ],
                            type=types.Function(
                                name="sum",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    )
                                ],
                                result=types.I32(),
                            ),
                            body=None,
                        ),
                    ],
                    type=types.Trait(name="List", functions=[]),
                )
            ],
            data_defs=[
                ast.DataDef(
                    name="EmptyList",
                    is_exported=False,
                    implements=["List"],
                    params=[],
                    functions=[
                        ast.Function(
                            name="length",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    ),
                                )
                            ],
                            type=types.Function(
                                name="length",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    )
                                ],
                                result=types.I32(),
                            ),
                            body=[ast.Number(value=0)],
                        ),
                        ast.Function(
                            name="sum",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    ),
                                )
                            ],
                            type=types.Function(
                                name="sum",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    )
                                ],
                                result=types.I32(),
                            ),
                            body=[ast.Number(value=0)],
                        ),
                    ],
                    type=types.Data(name="EmptyList", implements=[types.TypeRef("List")], fields=[], functions=[]),
                ),
                ast.DataDef(
                    name="Cons",
                    is_exported=False,
                    implements=["List"],
                    params=[
                        ast.Param(
                            name="head", type=types.Field(name="head", type=types.I32())
                        ),
                        ast.Param(
                            name="tail",
                            type=types.Field(
                                name="tail", type=types.TypeRef(name="List")
                            ),
                        ),
                    ],
                    functions=[
                        ast.Function(
                            name="length",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    ),
                                )
                            ],
                            type=types.Function(
                                name="length",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    )
                                ],
                                result=types.I32(),
                            ),
                            body=[
                                ast.BinaryOperation(
                                    operator=ast.BinaryOperator.ADD,
                                    left=ast.Number(value=1),
                                    right=ast.FunctionCall(
                                        name="self.tail.length", arguments=[]
                                    ),
                                )
                            ],
                        ),
                        ast.Function(
                            name="sum",
                            is_exported=False,
                            params=[
                                ast.Param(
                                    name="self",
                                    type=types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    ),
                                )
                            ],
                            type=types.Function(
                                name="sum",
                                params=[
                                    types.Param(
                                        name="self", type=types.TypeRef(name="List")
                                    )
                                ],
                                result=types.I32(),
                            ),
                            body=[
                                ast.BinaryOperation(
                                    operator=ast.BinaryOperator.ADD,
                                    left=ast.MemberAccess(
                                        value=ast.Variable(name="self"), member="head"
                                    ),
                                    right=ast.FunctionCall(
                                        name="self.tail.sum", arguments=[]
                                    ),
                                )
                            ],
                        ),
                    ],
                    type=types.Data(
                        name="Cons",
                        implements=[types.TypeRef("List")],
                        fields=[
                            types.Field(name="head", type=types.I32()),
                            types.Field(name="tail", type=types.TypeRef(name="List")),
                        ],
                        functions=[],
                    ),
                ),
            ],
            functions=[],
        ),
    )
