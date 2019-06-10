import antlr4
import pytest

from tests.helpers.wasm import assert_equal_modules
from wasm.model import (
    Module,
    Func,
    BinaryOperation,
    Call,
    Param,
    Const,
    Local,
    LocalSet,
    LocalGet,
    Result,
    If,
    Return,
    Import,
    GlobalSet,
    GlobalGet,
    Store,
    Load,
)
from compiler import compiler


def get_wasm(source: str) -> Module:
    input_stream = antlr4.InputStream(source)
    parse_tree = compiler.get_parse_tree(input_stream)
    ast = compiler.get_semantic_analysis(compiler.get_ast(parse_tree))
    return compiler.get_wasm(ast)


def test_empty_program():
    source = ""
    result = get_wasm(source)

    assert result == Module(imports=[], instructions=[])


def test_simple_expression():
    source = """
        import System::Output;

        export function Main(): void {
            println(value=1 + 2 * 3);
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[
                        Call(
                            name="$output_println",
                            arguments=[
                                BinaryOperation(
                                    op="i32.add",
                                    left=Const(type="i32", val="1"),
                                    right=BinaryOperation(
                                        op="i32.mul",
                                        left=Const(type="i32", val="2"),
                                        right=Const(type="i32", val="3"),
                                    ),
                                )
                            ],
                        )
                    ],
                )
            ],
        ),
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
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[Local(type="i32", name="$a"), Local(type="i32", name="$b")],
                    result=Result(type=None),
                    instructions=[
                        LocalSet(name="$a", val=Const(type="i32", val="5")),
                        LocalSet(name="$b", val=Const(type="i32", val="10")),
                        Call(
                            name="$output_println",
                            arguments=[
                                BinaryOperation(
                                    op="i32.add",
                                    left=LocalGet(name="$a"),
                                    right=LocalGet(name="$b"),
                                )
                            ],
                        ),
                    ],
                )
            ],
        ),
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
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$sayNumber",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    export=None,
                    instructions=[
                        Call(
                            name="$output_println",
                            arguments=[Const(type="i32", val="1337")],
                        )
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[Call(name="$sayNumber", arguments=[])],
                ),
            ],
        ),
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
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$add",
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    locals=[],
                    result=Result(type="i32"),
                    export=None,
                    instructions=[
                        BinaryOperation(
                            op="i32.add",
                            left=LocalGet(name="$x"),
                            right=LocalGet(name="$y"),
                        )
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$add",
                                    arguments=[
                                        Const(type="i32", val="5"),
                                        Const(type="i32", val="15"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
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
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[
                        If(
                            condition=BinaryOperation(
                                op="i32.gt_s",
                                left=Const(type="i32", val="5"),
                                right=Const(type="i32", val="10"),
                            ),
                            result=Result(type=None),
                            then_statements=[
                                Call(
                                    name="$output_println",
                                    arguments=[Const(type="i32", val="1")],
                                )
                            ],
                            else_statements=None,
                        )
                    ],
                )
            ],
        ),
    )


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
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[
                        If(
                            condition=BinaryOperation(
                                op="i32.lt_s",
                                left=Const(type="i32", val="5"),
                                right=Const(type="i32", val="10"),
                            ),
                            result=Result(type=None),
                            then_statements=[
                                Call(
                                    name="$output_println",
                                    arguments=[Const(type="i32", val="1")],
                                )
                            ],
                            else_statements=[
                                Call(
                                    name="$output_println",
                                    arguments=[Const(type="i32", val="0")],
                                )
                            ],
                        )
                    ],
                )
            ],
        ),
    )


@pytest.mark.skip(
    "Pending type checks on if statements, invalid wasm is currently generated."
)
def test_factorial():
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
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$factorial",
                    export=None,
                    params=[Param(type="i32", name="$n")],
                    locals=[],
                    result=Result(type="i32"),
                    instructions=[
                        If(
                            condition=BinaryOperation(
                                op="i32.eq",
                                left=LocalGet(name="$n"),
                                right=Const(type="i32", val="1"),
                            ),
                            result=Result(type=None),
                            then_statements=[
                                Return(expression=Const(type="i32", val="1"))
                            ],
                            else_statements=[
                                Return(
                                    expression=(
                                        BinaryOperation(
                                            op="i32.mul",
                                            left=LocalGet(name="$n"),
                                            right=(
                                                Call(
                                                    name="$factorial",
                                                    arguments=[
                                                        BinaryOperation(
                                                            op="i32.sub",
                                                            left=LocalGet(name="$n"),
                                                            right=Const(
                                                                type="i32", val="1"
                                                            ),
                                                        )
                                                    ],
                                                )
                                            ),
                                        )
                                    )
                                )
                            ],
                        )
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$factorial",
                                    arguments=[Const(type="i32", val="5")],
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
    )


def test_simple_predicates():
    source = """
        function isGreaterThan(left: i32, right: i32): boolean {
            left > right;
        }

        function isLessThan(left: i32, right: i32): boolean {
            left < right;
        }

        function and(left: boolean, right: boolean): boolean {
            left && right;
        }

        function or(left: boolean, right: boolean): boolean {
            left || right;
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[],
            instructions=[
                Func(
                    name="$isGreaterThan",
                    export=None,
                    params=[
                        Param(type="i32", name="$left"),
                        Param(type="i32", name="$right"),
                    ],
                    locals=[],
                    instructions=[
                        BinaryOperation(
                            op="i32.gt_s",
                            left=LocalGet(name="$left"),
                            right=LocalGet(name="$right"),
                        )
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$isLessThan",
                    export=None,
                    params=[
                        Param(type="i32", name="$left"),
                        Param(type="i32", name="$right"),
                    ],
                    locals=[],
                    instructions=[
                        BinaryOperation(
                            op="i32.lt_s",
                            left=LocalGet(name="$left"),
                            right=LocalGet(name="$right"),
                        )
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$and",
                    export=None,
                    params=[
                        Param(type="i32", name="$left"),
                        Param(type="i32", name="$right"),
                    ],
                    locals=[],
                    instructions=[
                        BinaryOperation(
                            op="i32.and",
                            left=LocalGet(name="$left"),
                            right=LocalGet(name="$right"),
                        )
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$or",
                    export=None,
                    params=[
                        Param(type="i32", name="$left"),
                        Param(type="i32", name="$right"),
                    ],
                    locals=[],
                    instructions=[
                        BinaryOperation(
                            op="i32.or",
                            left=LocalGet(name="$left"),
                            right=LocalGet(name="$right"),
                        )
                    ],
                    result=Result(type="i32"),
                ),
            ],
        ),
    )


def test_data_vector():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32)

        export function Main(): void {

        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GlobalGet(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GlobalGet(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    result=Result(type=None),
                    locals=[],
                    instructions=[],
                ),
            ],
        ),
    )


def test_data_vector_constructor():
    source = """
        import System::Output;

        data Vector(x: i32, y: i32)

        export function Main(): void {
            let vector = Vector(x=10, y=20);
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    locals=[],
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="0"),
                                )
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="4"),
                                )
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    result=Result(type=None),
                    params=[],
                    locals=[Local(type="i32", name="$vector")],
                    instructions=[
                        LocalSet(
                            name="$vector",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="10"),
                                    Const(type="i32", val="20"),
                                ],
                            ),
                        )
                    ],
                ),
            ],
        ),
    )


def test_data_vector_with_simple_function():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function length(self: Vector): i32 {
                42;
            }
        }

        export function Main(): void {

        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="0"),
                                )
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="4"),
                                )
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Vector.length",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[Const(type="i32", val="42")],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[],
                    result=Result(type=None),
                    instructions=[],
                ),
            ],
        ),
    )


def test_data_vector_with_simple_function_call():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function length(self: Vector): i32 {
                42;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.length());
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="0"),
                                )
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="4"),
                                )
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Vector.length",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[Const(type="i32", val="42")],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[Local(type="i32", name="$vector")],
                    result=Result(type=None),
                    instructions=[
                        LocalSet(
                            name="$vector",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="10"),
                                    Const(type="i32", val="20"),
                                ],
                            ),
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.length",
                                    arguments=[LocalGet(name="$vector")],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def test_data_vector_with_self_getter_method():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function getX(self: Vector): i32 {
                self.x;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.getX());
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="0"),
                                )
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="4"),
                                )
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Vector.getX",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=LocalGet("$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="0"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        )
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[Local(name="$vector", type="i32")],
                    result=Result(type=None),
                    instructions=[
                        LocalSet(
                            name="$vector",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="10"),
                                    Const(type="i32", val="20"),
                                ],
                            ),
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.getX",
                                    arguments=[LocalGet(name="$vector")],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def test_data_vector_with_self_getter_methods():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function getX(self: Vector): i32 {
                self.x;
            }

            function getY(self: Vector): i32 {
                self.y;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.getX());
            println(value=vector.getY());
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="0"),
                                )
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="4"),
                                )
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Vector.getX",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=LocalGet("$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="0"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        )
                    ],
                ),
                Func(
                    name="$Vector.getY",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=LocalGet("$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="1"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        )
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[Local(name="$vector", type="i32")],
                    result=Result(type=None),
                    instructions=[
                        LocalSet(
                            name="$vector",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="10"),
                                    Const(type="i32", val="20"),
                                ],
                            ),
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.getX",
                                    arguments=[LocalGet(name="$vector")],
                                )
                            ],
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.getY",
                                    arguments=[LocalGet(name="$vector")],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def test_data_vector_with_math():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function getDoubleY(self: Vector): i32 {
                self.y + self.y;
            }
        }

        export function Main(): void {
            let vector = Vector(x=10, y=20);
            println(value=vector.getDoubleY());
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="0"),
                                )
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=(
                                BinaryOperation(
                                    op="i32.add",
                                    left=GlobalGet(name="$self_pointer"),
                                    right=Const(type="i32", val="4"),
                                )
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                ),
                Func(
                    name="$Vector.getDoubleY",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    result=Result(type="i32"),
                    locals=[],
                    instructions=[
                        BinaryOperation(
                            op="i32.add",
                            left=Load(
                                type="i32",
                                location=BinaryOperation(
                                    op="i32.add",
                                    left=LocalGet("$self"),
                                    right=BinaryOperation(
                                        op="i32.mul",
                                        left=Const(type="i32", val="1"),
                                        right=Const(type="i32", val="4"),
                                    ),
                                ),
                            ),
                            right=Load(
                                type="i32",
                                location=BinaryOperation(
                                    op="i32.add",
                                    left=LocalGet("$self"),
                                    right=BinaryOperation(
                                        op="i32.mul",
                                        left=Const(type="i32", val="1"),
                                        right=Const(type="i32", val="4"),
                                    ),
                                ),
                            ),
                        )
                    ],
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[Local(name="$vector", type="i32")],
                    result=Result(type=None),
                    instructions=[
                        LocalSet(
                            name="$vector",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="10"),
                                    Const(type="i32", val="20"),
                                ],
                            ),
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.getDoubleY",
                                    arguments=[LocalGet(name="$vector")],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def test_data_vector_with_complex_function():
    source = """
        import System::Output;

        export data Vector(x: i32, y: i32) {
            function add(self: Vector, other: Vector): Vector {
                Vector(
                    x = self.x + other.x,
                    y = self.y + other.y
                );
            }

            function getX(self: Vector): i32 {
                self.x;
            }

            function getY(self: Vector): i32 {
                self.y;
            }
        }

        export function Main(): void {
            let vectorA = Vector(x=3, y=6);
            let vectorB = Vector(x=5, y=3);
            let vectorC = vectorA.add(other=vectorB);
            println(value=vectorC.getX());
            println(value=vectorC.getY());
        }
     """
    result = get_wasm(source)

    assert_equal_modules(
        result,
        Module(
            imports=[
                Import(
                    name="$output_println",
                    import_=("System::Output", "println"),
                    params=[Param(type="i32", name=None)],
                    result=Result(type=None),
                )
            ],
            instructions=[
                Func(
                    name="$Vector.new",
                    export=None,
                    params=[Param(type="i32", name="$x"), Param(type="i32", name="$y")],
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GlobalGet(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            ),
                            val=LocalGet(name="$x"),
                        ),
                        Store(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GlobalGet(name="$self_pointer"),
                                right=Const(type="i32", val="4"),
                            ),
                            val=LocalGet(name="$y"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$Vector.add",
                    export=None,
                    params=[
                        Param(type="i32", name="$self"),
                        Param(type="i32", name="$other"),
                    ],
                    locals=[],
                    instructions=[
                        Call(
                            name="$Vector.new",
                            arguments=[
                                BinaryOperation(
                                    op="i32.add",
                                    left=Load(
                                        type="i32",
                                        location=BinaryOperation(
                                            op="i32.add",
                                            left=LocalGet(name="$self"),
                                            right=BinaryOperation(
                                                op="i32.mul",
                                                left=Const(type="i32", val="0"),
                                                right=Const(type="i32", val="4"),
                                            ),
                                        ),
                                    ),
                                    right=Load(
                                        type="i32",
                                        location=BinaryOperation(
                                            op="i32.add",
                                            left=LocalGet(name="$other"),
                                            right=BinaryOperation(
                                                op="i32.mul",
                                                left=Const(type="i32", val="0"),
                                                right=Const(type="i32", val="4"),
                                            ),
                                        ),
                                    ),
                                ),
                                BinaryOperation(
                                    op="i32.add",
                                    left=Load(
                                        type="i32",
                                        location=BinaryOperation(
                                            op="i32.add",
                                            left=LocalGet(name="$self"),
                                            right=BinaryOperation(
                                                op="i32.mul",
                                                left=Const(type="i32", val="1"),
                                                right=Const(type="i32", val="4"),
                                            ),
                                        ),
                                    ),
                                    right=Load(
                                        type="i32",
                                        location=BinaryOperation(
                                            op="i32.add",
                                            left=LocalGet(name="$other"),
                                            right=BinaryOperation(
                                                op="i32.mul",
                                                left=Const(type="i32", val="1"),
                                                right=Const(type="i32", val="4"),
                                            ),
                                        ),
                                    ),
                                ),
                            ],
                        )
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$Vector.getX",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    locals=[],
                    instructions=[
                        Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=LocalGet(name="$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="0"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        )
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$Vector.getY",
                    export=None,
                    params=[Param(type="i32", name="$self")],
                    locals=[],
                    instructions=[
                        Load(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=LocalGet(name="$self"),
                                right=BinaryOperation(
                                    op="i32.mul",
                                    left=Const(type="i32", val="1"),
                                    right=Const(type="i32", val="4"),
                                ),
                            ),
                        )
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$Main",
                    export="Main",
                    params=[],
                    locals=[
                        Local(type="i32", name="$vectorA"),
                        Local(type="i32", name="$vectorB"),
                        Local(type="i32", name="$vectorC"),
                    ],
                    instructions=[
                        LocalSet(
                            name="$vectorA",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="3"),
                                    Const(type="i32", val="6"),
                                ],
                            ),
                        ),
                        LocalSet(
                            name="$vectorB",
                            val=Call(
                                name="$Vector.new",
                                arguments=[
                                    Const(type="i32", val="5"),
                                    Const(type="i32", val="3"),
                                ],
                            ),
                        ),
                        LocalSet(
                            name="$vectorC",
                            val=Call(
                                name="$Vector.add",
                                arguments=[
                                    LocalGet(name="$vectorA"),
                                    LocalGet(name="$vectorB"),
                                ],
                            ),
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.getX",
                                    arguments=[LocalGet(name="$vectorC")],
                                )
                            ],
                        ),
                        Call(
                            name="$output_println",
                            arguments=[
                                Call(
                                    name="$Vector.getY",
                                    arguments=[LocalGet(name="$vectorC")],
                                )
                            ],
                        ),
                    ],
                    result=Result(type=None),
                ),
            ],
        ),
    )


def test_simple_trait():
    source = """
        trait EqualAge {
            function isEqualAge(self: EqualAge, age: i32): boolean;
        }

        data Person(age: i32) implements EqualAge {
            function isEqualAge(self: Person, age: i32): boolean {
                self.age == age;
            }
        }
     """
    result = get_wasm(source)

    import prettyprinter

    prettyprinter.pprint(result)

    assert_equal_modules(
        result,
        Module(
            imports=[],
            instructions=[
                Func(
                    name="$Person.new",
                    export=None,
                    params=[Param(type="i32", name="$age")],
                    locals=[],
                    instructions=[
                        GlobalSet(
                            name="$self_pointer",
                            val=Call(
                                name="$malloc", arguments=[Const(type="i32", val="2")]
                            ),
                        ),
                        Store(
                            type="i32",
                            location=BinaryOperation(
                                op="i32.add",
                                left=GlobalGet(name="$self_pointer"),
                                right=Const(type="i32", val="0"),
                            ),
                            val=LocalGet(name="$age"),
                        ),
                        GlobalGet(name="$self_pointer"),
                    ],
                    result=Result(type="i32"),
                ),
                Func(
                    name="$Person.isEqualAge",
                    export=None,
                    params=[
                        Param(type="i32", name="$self"),
                        Param(type="i32", name="$age"),
                    ],
                    locals=[],
                    instructions=[
                        BinaryOperation(
                            op="i32.eq",
                            left=Load(
                                type="i32",
                                location=BinaryOperation(
                                    op="i32.add",
                                    left=LocalGet(name="$self"),
                                    right=BinaryOperation(
                                        op="i32.mul",
                                        left=Const(type="i32", val="0"),
                                        right=Const(type="i32", val="4"),
                                    ),
                                ),
                            ),
                            right=LocalGet(name="$age"),
                        )
                    ],
                    result=Result(type="i32"),
                ),
            ],
        ),
    )
